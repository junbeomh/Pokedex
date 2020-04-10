"""

"""

import asyncio
from abc import ABC, abstractmethod
from pokemonretriever.pokedex_request import PokedexAPI
from pokemonretriever.pokedex_object import Pokemon, PokemonStat, \
    PokemonMove, PokemonAbility
from pokemonretriever.pokedex_parser import PokedexMoveParser, \
    PokedexStatParser, PokedexAbilityParser


class PokedexObjectFactory(ABC):

    def __init__(self, data_set: dict, is_expanded: bool = False):
        self.data_set = data_set
        self.is_expanded = is_expanded

    @abstractmethod
    def create(self):
        pass


class PokemonStatFactory(PokedexObjectFactory):

    def __init__(self, data: dict, is_expanded: bool):
        super().__init__(data, is_expanded)

    def create(self):
        for data in self.data_set:
            yield PokemonStat(**data)


class PokemonMoveFactory(PokedexObjectFactory):

    def __init__(self, data: dict, is_expanded: bool):
        super().__init__(data, is_expanded)

    def create(self):
        for data in self.data_set:
            yield PokemonMove(**data)


class PokemonAbilityFactory(PokedexObjectFactory):

    def __init__(self, data: dict, is_expanded: bool):
        super().__init__(data, is_expanded)

    def create(self):
        for data in self.data_set:
            yield PokemonAbility(**data)


class PokemonFactory(PokedexObjectFactory):

    def __init__(self, data: dict, is_expanded: bool):
        super().__init__(data, is_expanded)
        self.api = PokedexAPI()

    def create(self):
        if self.is_expanded:
            return self.create_mode_expanded()
        else:
            pokemon = Pokemon(**self.data_set)
            return pokemon

    def create_mode_expanded(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        pokemon = Pokemon(**self.data_set)
        ability_name = self.data_set["abilities"][0]["ability"]['name']
        move_name = self.data_set["moves"][0]['move']['name']
        stat_number = self.data_set["stats"][0]["stat"]["url"][-2]
        pokemon.stats = self.add_expanded_stats(stat_number)
        pokemon.moves = self.add_expanded_moves(move_name)
        pokemon.abilities = self.add_expanded_abilities(ability_name)
        return pokemon

    def add_expanded_abilities(self, name):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        ability = loop.run_until_complete(self.api.process_single_request(
            "ability", name))
        pokemon_ability = PokedexAbilityParser.parse(ability, name)
        return PokemonAbility(**pokemon_ability)

    def add_expanded_moves(self, name):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        move = loop.run_until_complete(self.api.process_single_request(
            "move", name))
        pokemon_move = PokedexMoveParser.parse(move, name)
        return PokemonMove(**pokemon_move)

    def add_expanded_stats(self, number):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        stat = loop.run_until_complete(self.api.process_single_request(
            "stat", number))
        pokemon_stat = PokedexStatParser.parse(json=stat)
        return PokemonStat(**pokemon_stat)


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
