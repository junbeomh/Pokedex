"""
Contains the class definition of a PokemonObjectFactory ABC class and
its child class.
"""

import asyncio
from abc import ABC, abstractmethod
from pokemonretriever.pokedex_request import PokedexAPI
from pokemonretriever.pokedex_object import Pokemon, PokemonStat, \
    PokemonMove, PokemonAbility
from pokemonretriever.pokedex_parser import PokedexMoveParser, \
    PokedexStatParser, PokedexAbilityParser, PokedexPokemonParser


class PokedexObjectFactory(ABC):
    """
    Represents a factory class to instantiate PokemonObjects
    """
    def __init__(self, data_set: list, is_expanded: bool = False):
        """
        Instantiates a PokemonObjectFactory.
        :param data_set: a list
        :param is_expanded: a boolean
        """
        self.data_set = data_set
        self.is_expanded = is_expanded

    @abstractmethod
    def create(self):
        """
        Instantiates a PokemonObject.
        :return:
        """
        pass


class PokemonStatFactory(PokedexObjectFactory):
    """
    Represents a Factory to instantiate Stat Objects.
    """
    def __init__(self, data: list, is_expanded: bool):
        """
        Instantiates a PokemonStatFactory.
        :param data: a list
        :param is_expanded: a boolean
        """
        super().__init__(data, is_expanded)

    def create(self):
        """
        Instantiates Stat Objects.
        :return:
        """
        for data in self.data_set:
            stat_praser = PokedexStatParser().parse(data)
            yield PokemonStat(**stat_praser)


class PokemonMoveFactory(PokedexObjectFactory):
    """
    Represents a Factory that instantiates Move Objects.
    """
    def __init__(self, data: list, is_expanded: bool):
        """
        Instantiates a PokemonMoveFactory.
        :param data: a list
        :param is_expanded: a boolean
        """
        super().__init__(data, is_expanded)

    def create(self):
        """
        Instantiates Move Objects.
        :return:
        """
        for data in self.data_set:
            move_parser = PokedexMoveParser().parse(data)
            yield PokemonMove(**move_parser)


class PokemonAbilityFactory(PokedexObjectFactory):
    """
    Represents a Factory that instantiates Ability Objects.
    """
    def __init__(self, data: list, is_expanded: bool):
        """
        Instantiates a PokemonAbilityFactory
        :param data: a list
        :param is_expanded: a boolean
        """
        super().__init__(data, is_expanded)

    def create(self):
        """
        Instantiates Ability Objects
        :return:
        """
        for data in self.data_set:
            ability_parser = PokedexAbilityParser().parse(data)
            yield PokemonAbility(**ability_parser)


class PokemonFactory(PokedexObjectFactory):
    """
    Represents a Factory that instantiates Pokemon Objects.
    """
    def __init__(self, data: list, is_expanded: bool):
        """
        Instantiates a PokemonFactory
        :param data: a list
        :param is_expanded: a bool
        """
        super().__init__(data, is_expanded)
        self.api = PokedexAPI()

    def create(self):
        """
        Instantiates Pokemon Objets.
        :return:
        """
        if self.is_expanded:
            return self.create_mode_expanded()
        else:
            return self.create_mode_normal()

    def create_mode_normal(self):
        """
        Instantiates Pokemon Objets when --expanded is not used in the terminal
        command.
        :return:
        """
        for data in self.data_set:
            pokemon_parcer = PokedexPokemonParser.parse(data)
            yield Pokemon(**pokemon_parcer)

    def create_mode_expanded(self):
        """
        Instantiates Pokemon, Ability, Move, and Stat Objects if --expanded
        is used in the terminal command
        :return:
        """
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
            pokemon.stats = self.__add_expanded_stats(stats_name)
            pokemon.moves = self.__add_expanded_moves(move_name)
            pokemon.abilities = self.__add_expanded_abilities(ability_name)
            yield pokemon

    def __add_expanded_stats(self, number):
        """
        Instantiates Stat Objects for Pokemon created by the PokemonFactory.
        :param number: a list
        :return: a list
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        stats = loop.run_until_complete(self.api.process_requests(
            "stat", number))
        stat_list = []
        factory = PokemonStatFactory(stats, True)
        for stat in factory.create():
            stat_list.append(stat)
        return stat_list

    def __add_expanded_abilities(self, name):
        """
        Instantiates Ability Objects for Pokemon created by the PokemonFactory.
        :param name: a list
        :return: a list
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        abilities = loop.run_until_complete(self.api.process_requests(
            "ability", name))
        ability_list = []
        factory = PokemonAbilityFactory(abilities, True)
        for ability in factory.create():
            ability_list.append(ability)
        return ability_list

    def __add_expanded_moves(self, name):
        """
        Instantiates Move Objects for Pokemon created by the PokemonFactory.
        :param name: a list
        :return: a list
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        moves = loop.run_until_complete(self.api.process_requests(
            "move", name))
        move_list = []
        factory = PokemonMoveFactory(moves, True)
        for move in factory.create():
            move_list.append(move)
        return move_list
