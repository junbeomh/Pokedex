from abc import ABC


class PokedexObject(ABC):

    def __init__(self, name: str, id: int, **kwargs):
        self.name = name.title()
        self.id = id


class Pokemon(PokedexObject):
    """
    """

    def __init__(self, name: str, id: int, height: int, weight: int,
                 types: [str], stats: list, abilities: [list],
                 moves: list, **kwargs):
        """
        """
        super().__init__(name, id, **kwargs)
        self.height = height
        self.weight = weight
        self.type = self.parse_pokemon_type(types)
        self.stats = self.parse_stats(stats)
        self.stats = stats
        self.abilities = self.parse_abilities(abilities)
        self.abilities = abilities

        self.moves = self.parse_moves(moves)
        self.moves = moves

    @staticmethod
    def parse_pokemon_type(types: list):
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
    def parse_stats(stats: list):
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
    def parse_abilities(abilities: list):
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
    def parse_moves(moves: list):
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
        return f"Pokemon: {self.name}\n" \
               f"ID: {self.id}\n" \
               f"Height: {self.height}\n" \
               f"Weight: {self.weight}\n"
               # f"Type: {', '.join(self.type)}\n" \
               # f"Stats: {self.stats}\n" \
               # f"Abilities: {', '.join(self.abilities)}\n" \
               # f"Moves: {self.moves}\n"


class PokemonAbility(PokedexObject):

    def __init__(self, name: str, id: int, generation: str,
                 effect: str, effect_short: str, pokemon: list, **kwargs):
        super().__init__(name, id, **kwargs)
        self.generation = generation

        # removes double space btwn lines
        self.effect = effect.replace('\n\n', '')

        self.effect_short = effect_short
        self.pokemon = self.parse_pokemon(pokemon)

    @staticmethod
    def parse_pokemon(pokemons: list):
        output = []
        for pokemon in pokemons:
            output.append(pokemon["pokemon"]["name"])
        return output

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

    def __init__(self, name: str, id: int, is_battle_only: bool,
                 **kwargs):
        super().__init__(name, id, **kwargs)
        self.is_battle_only = is_battle_only

    def __str__(self):
        return f"Stat: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Is Battle Only: {self.is_battle_only}\n"


class PokemonMove(PokedexObject):

    def __init__(self, name: str, id: int, generation: str, accuracy: int,
                 pp: int, power: int, move_type: str, dmg_class: str,
                 effect_short: str, **kwargs):
        super().__init__(name, id, **kwargs)
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
