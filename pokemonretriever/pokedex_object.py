"""
Contains the class definition for PokedexObjects and its child classes.
"""
from abc import ABC


class PokedexObject(ABC):
    """
    Represents an item in the pokedex.
    """
    def __init__(self, name: str, id: int):
        """
        Instantiates a PokedexObject.
        :param name: a string
        :param id: an int
        """
        self.name = name.title()
        self.id = id


class Pokemon(PokedexObject):
    """
    Represents a pokemon in the pokedex.
    """
    def __init__(self, height: int, weight: int,
                 types: [str], stats: list, abilities: [list],
                 moves: list, **kwargs):
        """
        Instantiztes a Pokemon.
        :param height: an int
        :param weight: an int
        :param types: a list of strings
        :param stats: a list of stats
        :param abilities: a list of abilities
        :param moves: a list of moves
        :param kwargs: a dictionary of named arguments and values.
        """
        super().__init__(**kwargs)
        self.height = height
        self.weight = weight
        self.type = self.__format_pokemon_type(types)
        self.stats = self.__format_stats(stats)
        self.abilities = self.__format_abilities(abilities)
        self.moves = self.__format_moves(moves)

    @staticmethod
    def __format_pokemon_type(types: list):
        """
        Parses the Pokemon's raw type data into a processable
        default format.

        :param types: a list of dict that contains the API data about
                      the pokemon's type.
        :return: a list of string that contain information
                 about the pokemon's type.
        """
        output = []
        for pokemon_type in types:
            output.append(pokemon_type['type']['name'])
        return output

    @staticmethod
    def __format_stats(stats: list):
        """
        Parses the Pokemon's raw stats data into a processable
        default format.

        :param stats: a list of dict that contains the API data about
                      the pokemon.
        :return: a list of tuples that contain information about
                 the pokemon's stats.
        """
        output = []
        for stat in stats:
            base_stat = ""
            name = ""
            for key, value in stat.items():
                if key == 'base_stat':
                    base_stat = value
                if key == 'stat':
                    name = value['name']
            output.append((name, base_stat))
        return output

    @staticmethod
    def __format_abilities(abilities: list):
        """
        Parses the Pokemon's raw ability data into a processable
        default format.

        :param abilities: a list of dict that contains the API data about
                          the pokemon.
        :return: a list of strings that contain information
                 about the pokemon's ability
        """
        output = []
        for ability in abilities:
            output.append(ability['ability']['name'])
        return output

    @staticmethod
    def __format_moves(moves: list):
        """
        Parses the Pokemon's raw attacking move data into a
        processable default format.

        :param moves: a list of dict that contains the API data about
                      the pokemon.
        :return: a list of tuples that contain information about
                 the pokemon's attack moves.
        """
        output = []
        for move in moves:
            name = ""
            level_learned = ""
            for key, value in move.items():
                if key == 'move':
                    name = value['name']
                if key == 'version_group_details':
                    level_learned = value[0]['level_learned_at']
            output.append((name, level_learned))
        return output

    def __str__(self):
        """
        Returns a string representation of a pokemon.
        :return: a string
        """
        formatted = "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        formatted += f"Pokemon: {self.name}\n" \
                     f"ID: {self.id}\n" \
                     f"Weight: {self.weight}\n"\
                     f"Type: {self.type}\n"
        if isinstance(self.stats[0], PokemonStat):
            formatted += "\n<Pokemon Stats>\n"
            stats = [str(stat) for stat in self.stats]
            formatted += ''.join(stats)
            formatted += "</Pokemon Stats>\n"
        else:
            formatted += f"Stats: {self.stats}\n"
        if isinstance(self.moves[0], PokemonMove):
            formatted += "\n<Pokemon Moves>\n"
            moves = [str(move) for move in self.moves]
            formatted += ''.join(moves)
            formatted += "</Pokemon Moves>\n"
        else:
            formatted += f"Moves: {self.moves}\n"
        if isinstance(self.abilities[0], PokemonAbility):
            formatted += "\n<Pokemon Abilities>\n"
            abilities = [str(ability) for ability in self.abilities]
            formatted += ''.join(abilities)
            formatted += "</Pokemon Abilities>\n"
        else:
            formatted += f"Abilities: {', '.join(self.abilities)}\n"
        formatted += "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n"
        return formatted


class PokemonAbility(PokedexObject):
    """
    Represents an ability in the pokedex.
    """
    def __init__(self, name: str, id: int, generation: str,
                 effect: str, effect_short: str, pokemon: list, **kwargs):
        """
        Instantiates a PokemonAbility.
        :param name: a string
        :param id: an int
        :param generation: a string
        :param effect: a string
        :param effect_short: a string
        :param pokemon: a list of pokemon
        :param kwargs: a dictionary of named arguments and values.
        """
        super().__init__(name, id, **kwargs)
        self.generation = generation
        # removes double space btwn lines
        self.effect = effect.replace('\n\n', '')
        self.effect_short = effect_short
        self.pokemon = self.__format_pokemon(pokemon)

    @staticmethod
    def __format_pokemon(pokemons: list):
        """
        Parses the list of pokemon into a processable default format.
        :param pokemons: a list
        :return: a list
        """
        output = []
        for pokemon in pokemons:
            output.append(pokemon["pokemon"]["name"])
        return output

    @staticmethod
    def __format_list(lines: str) -> str:
        """
        Parses lines into a processable default format.
        :param lines: a string
        :return: a string
        """
        lines_list = lines.split(".")
        formatted_output = ""
        for line in lines_list:
            if not line == "":
                line += ". "
                formatted_output += line
        return formatted_output

    def __str__(self):
        """
        Returns a string representation of an Ability.
        :return: a string
        """
        return f"-----------------------------------\n" \
               f"Ability: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Generation: {self.generation}\n" \
               f"Short Effect: {self.effect_short}\n" \
               f"Effect: {self.__format_list(self.effect)}\n" \
               f"Pokemon: {self.pokemon}\n"


class PokemonStat(PokedexObject):
    """
    Represents a stat in the pokedex.
    """
    def __init__(self, is_battle_only: bool, **kwargs):
        """
        Instantiates a stat.
        :param is_battle_only: a boolean
        :param kwargs: a dictionary of named arguments and values.
        """
        super().__init__(**kwargs)
        self.is_battle_only = is_battle_only

    def __str__(self):
        """
        Returns a string representation of a Stat.
        :return: a string
        """
        return f"-----------------------------------\n" \
               f"Stat: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Is Battle Only: {self.is_battle_only}\n"


class PokemonMove(PokedexObject):
    """
    Represents a move in the pokedex.
    """
    def __init__(self, name: str, id: int, generation: str, accuracy: int,
                 pp: int, power: int, type: str, damage_class: str,
                 effect_short: str, **kwargs):
        """
        Instantiates a move.
        :param name: a string
        :param id: an int
        :param generation: a string
        :param accuracy: an int
        :param pp: an int
        :param power: an int
        :param type: a string
        :param damage_class: a string
        :param effect_short: a string
        :param kwargs: a dictionary of named arguments and values.
        """
        super().__init__(name, id, **kwargs)
        self.generation = generation
        self.accuracy = accuracy
        self.effect_short = effect_short
        self.pp = pp
        self.power = power
        self.type = type
        self.damage_class = damage_class

    def __str__(self):
        """
        Returns a string represntation of a move.
        :return: a string
        """
        return f"-----------------------------------\n" \
               f"Move: : {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Generation: {self.generation}\n" \
               f"Accuracy: {self.accuracy}\n" \
               f"PP: {self.pp}\n" \
               f"Power: {self.power}\n" \
               f"Type: {self.type}\n" \
               f"Damage class: {self.damage_class}\n" \
               f"Effect: {self.effect_short}\n"
