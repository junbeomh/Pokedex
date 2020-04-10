"""

"""


class PokedexParser:

    def __init__(self):
        self.output = None

    def parse_pokemon_type(self, types: list):
        """
        Parses the Pokemon's raw type data into a processable
        default format.

        :param types: a list of dict that contains the API data about
                      the pokemon's type.
        :return: a list of string that contain information
                 about the pokemon's type.
        """
        self.output = []
        for pokemon_type in types:
            self.output.append(pokemon_type['type']['name'])
        return self.output

    def parse_pokemon_default_stat(self, stats: list):
        """
        Parses the Pokemon's raw stats data into a processable
        default format.

        :param stats: a list of dict that contains the API data about
                      the pokemon.
        :return: a list of tuples that contain information about
                 the pokemon's stats.
        """
        self.output = []
        for stat in stats:
            base_stat = ""
            name = ""
            for key, value in stat.items():
                if key == 'base_stat':
                    base_stat = value
                if key == 'stat':
                    name = value['name']
            self.output.append((name, base_stat))
        return self.output

    def parse_pokemon_default_abilities(self, abilities: list):
        """
        Parses the Pokemon's raw ability data into a processable
        default format.

        :param abilities: a list of dict that contains the API data about
                          the pokemon.
        :return: a list of strings that contain information
                 about the pokemon's ability
        """
        self.output = []
        for ability in abilities:
            self.output.append(ability['ability']['name'])
        return self.output

    def parse_pokemon_default_moves(self, moves: list):
        """
        Parses the Pokemon's raw attacking move data into a
        processable default format.

        :param moves: a list of dict that contains the API data about
                      the pokemon.
        :return: a list of tuples that contain information about
                 the pokemon's attack moves.
        """
        self.output = []
        for move in moves:
            name = ""
            level_learned = ""
            for key, value in move.items():
                if key == 'move':
                    name = value['name']
                if key == 'version_group_details':
                    level_learned = value[0]['level_learned_at']
            self.output.append((name, level_learned))
        return self.output

    def parse_pokemon(self, pokemons: list):
        self.output = []
        for pokemon in pokemons:
            self.output.append(pokemon["pokemon"]["name"])
        return self.output

    def parse_ability_effect(self, effects: str):
        pass
