class Pokemon:
    """
    A class for a pokemon entity.
    """

    def __init__(self, pokemon_id: str, name: str, height: str, weight: str,
                 pokemon_type: list, stats: list, abilities: list,
                 moves: list):
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
        self.id = pokemon_id
        self.name = name
        self.height = height
        self.weight = weight
        self.type = self.parse_types(pokemon_type)
        self.stats = self.parse_default_stats(stats)
        self.abilities = self.parse_default_abilities(abilities)
        self.moves = self.parse_default_moves(moves)

    @staticmethod
    def parse_types(types: list):
        """
        Parses the Pokemon's raw type data into a processable
        default format.

        :param types: a list of dict that contains the API data about
                      the pokemon's type.
        :return: a list of string that contain information
                 about the pokemon's type.
        """
        type_lists = []
        for pokemon_type in types:
            type_lists.append(pokemon_type['type']['name'])
        return type_lists

    @staticmethod
    def parse_default_stats(stats: list):
        """
        Parses the Pokemon's raw stats data into a processable
        default format.

        :param stats: a list of dict that contains the API data about
                      the pokemon.
        :return: a list of tuples that contain information about
                 the pokemon's stats.
        """
        stat_list = []
        for stat in stats:
            base_stat = ""
            name = ""
            for key, value in stat.items():
                if key == 'base_stat':
                    base_stat = value
                if key == 'stat':
                    name = value['name']
            stat_list.append((name, base_stat))
        return stat_list

    @staticmethod
    def parse_default_abilities(abilities: list):
        """
        Parses the Pokemon's raw ability data into a processable
        default format.

        :param abilities: a list of dict that contains the API data about
                          the pokemon.
        :return: a list of strings that contain information
                 about the pokemon's ability
        """
        ability_list = []
        for ability in abilities:
            ability_list.append(ability['ability']['name'])
        return ability_list

    @staticmethod
    def parse_default_moves(moves: list):
        """
        Parses the Pokemon's raw attacking move data into a
        processable default format.

        :param moves: a list of dict that contains the API data about
                      the pokemon.
        :return: a list of tuples that contain information about
                 the pokemon's attack moves.
        """
        move_list = []
        for move in moves:
            name = ""
            level_learned = ""
            for key, value in move.items():
                if key == 'move':
                    name = value['name']
                if key == 'version_group_details':
                    level_learned = value[0]['level_learned_at']
            move_list.append((name, level_learned))
        return move_list

    def __str__(self):
        return f"Pokemon: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Height: {self.height}\n" \
               f"Weight: {self.weight}\n" \
               f"Type: {', '.join(self.type)}\n" \
               f"Stats: {self.stats}\n" \
               f"Abilities: {', '.join(self.abilities)}\n" \
               f"Moves: {self.moves}\n" \
