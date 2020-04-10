from abc import ABC
from pokemonretriever.pokedex_parser import PokedexParser


class PokedexObject(ABC):
    def __init__(self, name: str, id: int, **kwargs):
        self.name = name
        self.id = id
        self.parser = PokedexParser()
        super().__init__(**kwargs)


class Pokemon(PokedexObject):
    """
    A class for a pokemon entity.
    """

    def __init__(self, name: str, pokemon_id: int, height: int, weight: int,
                 pokemon_type: list, stats: list, abilities: list,
                 moves: list, **kwargs):
        """
        Initializes a Pokemon object.

        :param pokemon_id: a string.
        :param name: a string.
        :param height: a string.
        :param weight: a string.
        :param pokemon_type: a list of string that contain information
                             about the pokemon's type.
        :param stats: a list of tuples that contain information about
                      the pokemon's stats.
        :param abilities: a list of strings that contain information
                          about the pokemon's ability
        :param moves: a list of tuples that contain information about
                      the pokemon's attack moves.
        """
        super().__init__(name, pokemon_id, **kwargs)
        self.height = height
        self.weight = weight
        self.type = self.parser.parse_pokemon_type(pokemon_type)
        self.stats = self.parser.parse_pokemon_default_stat(stats)
        self.abilities = self.parser.parse_pokemon_default_abilities(abilities)
        self.moves = self.parser.parse_pokemon_default_moves(moves)

    def __str__(self):
        return f"Pokemon: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Height: {self.height}\n" \
               f"Weight: {self.weight}\n" \
               f"Type: {', '.join(self.type)}\n" \
               f"Stats: {self.stats}\n" \
               f"Abilities: {', '.join(self.abilities)}\n" \
               f"Moves: {self.moves}\n"


class PokemonAbility(PokedexObject):
    def __init__(self, name: str, ability_id: int, generation: str,
                 effect: str, effect_short: str, pokemons: list, **kwargs):
        super().__init__(name, ability_id, **kwargs)
        self.generation = generation

        # removes double space btwn lines
        self.effect = effect.replace('\n\n', '')

        self.effect_short = effect_short
        self.pokemon = self.parser.parse_pokemon(pokemons)

    @staticmethod
    def format_list(lines: str) -> str:
        lines_list = lines.split(".")
        formatted_output = ""
        for line in lines_list:
            if not line == "":
                line += ". "
                formatted_output += line
        return formatted_output

    def __str__(self):
        return f"Ability: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Generation: {self.generation}\n" \
               f"Short Effect: {self.effect_short}\n" \
               f"Effect: {self.format_list(self.effect)}\n" \
               f"Pokemon: {self.pokemon}\n"


class PokemonStat(PokedexObject):
    def __init__(self, name: str, stat_id: int, is_battle_only: bool,
                 **kwargs):
        super().__init__(name, stat_id, **kwargs)
        self.is_battle_only = is_battle_only

    def __str__(self):
        return f"Stat: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Is Battle Only: {self.is_battle_only}\n"


class PokemonMove(PokedexObject):

    def __init__(self, name: str, move_id: int, generation: str, accuracy: int,
                 pp: int, power: int, move_type: str, dmg_class: str,
                 effect_short: str, **kwargs):
        super().__init__(name, move_id, **kwargs)
        self.generation = generation
        self.accuracy = accuracy
        self.effect_short = effect_short
        self.pp = pp
        self.power = power
        self.move_type = move_type
        self.dmg_class = dmg_class

    def __str__(self):
        return f"Move: : {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Generation: {self.generation}\n" \
               f"Accuracy: {self.accuracy}\n" \
               f"PP: {self.pp}\n" \
               f"Power: {self.power}\n" \
               f"Type: {self.move_type}\n" \
               f"Damage class: {self.dmg_class}\n" \
               f"Effect: {self.effect_short}\n"
