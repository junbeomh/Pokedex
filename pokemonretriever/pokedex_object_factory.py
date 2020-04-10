"""

"""

import asyncio
from abc import ABC, abstractmethod
from pokemonretriever.pokedex_request import PokedexAPI
from pokemonretriever.pokedex_object import Pokemon, PokemonStat, \
    PokemonMove, PokemonAbility
from pokemonretriever.pokedex_parser import PokedexMoveParser, \
    PokedexStatParser, PokedexAbilityParser, PokedexPokemonParser


class PokedexObjectFactory(ABC):
    def __init__(self, data_set: list, is_expanded: bool = False):
        self.data_set = data_set
        self.is_expanded = is_expanded

    @abstractmethod
    def create(self):
        pass


class PokemonStatFactory(PokedexObjectFactory):

    def __init__(self, data: list, is_expanded: bool):
        super().__init__(data, is_expanded)

    def create(self):
        print(len(self.data_set))
        for data in self.data_set:
            stat_praser = PokedexStatParser().parse(data)
            yield PokemonStat(**stat_praser)


class PokemonMoveFactory(PokedexObjectFactory):

    def __init__(self, data: list, is_expanded: bool):
        super().__init__(data, is_expanded)

    def create(self):
        for data in self.data_set:
            move_parser = PokedexMoveParser().parse(data)
            yield PokemonMove(**move_parser)


class PokemonAbilityFactory(PokedexObjectFactory):

    def __init__(self, data: list, is_expanded: bool):
        super().__init__(data, is_expanded)

    def create(self):
        for data in self.data_set:
            ability_parser = PokedexAbilityParser().parse(data)
            yield PokemonAbility(**ability_parser)


class PokemonFactory(PokedexObjectFactory):

    def __init__(self, data: list, is_expanded: bool):
        super().__init__(data, is_expanded)
        self.api = PokedexAPI()

    def create(self):
        if self.is_expanded:
            return self.create_mode_expanded()
        else:
            return self.create_mode_normal()

    def create_mode_normal(self):
        print(len(self.data_set))
        for data in self.data_set:
            pokemon_parcer = PokedexPokemonParser.parse(data)
            yield Pokemon(**pokemon_parcer)

    def create_mode_expanded(self):
        for data in self.data_set:
            pokemon_parcer = PokedexPokemonParser.parse(data)
            pokemon = Pokemon(**pokemon_parcer)
            ability_name = []
            move_name = []
            stats_name = []
            for i in range(0, len(data["abilities"])):
                ability_name.append(data["abilities"][i]["ability"]['name'])
            for i in range(0, len(data["moves"])):
                move_name.append(data["moves"][i]['move']['name'])
            for i in range(0, len(data["stats"])):
                stats_name.append(data["stats"][i]["stat"]["url"][-2])
            print(stats_name)
            pokemon.stats = self.add_expanded_stats(stats_name)
            pokemon.moves = self.add_expanded_moves(move_name)
            pokemon.abilities = self.add_expanded_abilities(ability_name)
            yield pokemon

    def add_expanded_abilities(self, name):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        abilities = loop.run_until_complete(self.api.process_requests(
            "ability", name))
        ability_list = []
        factory = PokemonAbilityFactory(abilities, True)
        for ability in factory.create():
            ability_list.append(ability)
        return ability_list

    def add_expanded_moves(self, name):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        moves = loop.run_until_complete(self.api.process_requests(
            "move", name))
        move_list = []
        factory = PokemonMoveFactory([moves], True)
        for move in factory.create():
            move_list.append(move)
        return move_list

    def add_expanded_stats(self, number):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        stats = loop.run_until_complete(self.api.process_requests(
            "stat", number))
        stat_list = []
        factory = PokemonStatFactory([stats], True)
        for stat in factory.create():
            stat_list.append(stat)
        return stat_list


def main():
    pokedex = PokedexAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    pokemons = loop.run_until_complete(pokedex.process_single_request(
        "pokemon", "151"))
    factory = PokemonFactory(pokemons, True)
    pokemon = factory.create()
    print(pokemon.stats)
    print(pokemon.moves)
    print(pokemon.abilities)


if __name__ == "__main__":
    main()
