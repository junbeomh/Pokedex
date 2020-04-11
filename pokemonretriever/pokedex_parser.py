"""

"""

from abc import ABC, abstractmethod


class PokedexDataParser(ABC):

    def __init__(self):
        self.json = None

    @staticmethod
    @abstractmethod
    def parse(json, value):
        pass


class PokedexPokemonParser(PokedexDataParser):
    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(json):
        pokemon = json
        name = pokemon["name"]
        id = int(pokemon["id"])
        height = int(pokemon["height"])
        weight = int(pokemon["weight"])
        types = pokemon["types"]
        stats = pokemon["stats"]
        abilities = pokemon["abilities"]
        moves = pokemon["moves"]
        return {'name': name, 'id': id, 'height': height, 'weight': weight,
                'types': types, 'stats': stats, 'abilities': abilities,
                'moves': moves}


class PokedexAbilityParser(PokedexDataParser):

    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(json):
        ability = json
        name = ability["name"]
        id = int(ability["id"])
        generation = ability["generation"]["name"]
        effect = ability["effect_entries"][0]["effect"]
        effect_short = ability["effect_entries"][0]["short_effect"]
        pokemon = ability["pokemon"]
        return {'name': name, 'id': id, 'generation': generation,
                'effect': effect, 'effect_short': effect_short,
                'pokemon': pokemon}


class PokedexStatParser(PokedexDataParser):

    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(json, value=None):
        stat = json
        name = stat["name"]
        id = stat["id"]
        is_battle_only = stat["is_battle_only"]
        return {'name': name, 'id': id, "is_battle_only": is_battle_only}


class PokedexMoveParser(PokedexDataParser):

    def __init__(self):
        super().__init__()

    @staticmethod
    def parse(json):
        move = json
        name = move["name"]
        id = int(move['id']),
        generation = move['generation']['name'],
        accuracy = move['accuracy'],
        pp = int(move['pp']),
        power = move['power'],
        move_type = move['type']['name'],
        dmg_class = move['damage_class']['name'],
        effect_short = move['effect_entries'][0]['short_effect']
        return {'name': name, 'id': id, 'generation': generation,
                "accuracy": accuracy, "pp": pp, "power": power,
                "type": move_type, "damage_class": dmg_class,
                'effect_short': effect_short}

    # def parse_ability(self, name):
    #     ability = self.json
    #     name = name
    #     id = int(ability["id"])
    #     generation = ability["generation"]["name"]
    #     effect = ability["effect_entries"][0]["effect"]
    #     effect_short = ability["effect_entries"][0]["short_effect"]
    #     pokemon = ability["pokemon"]
    #     return {'name': name, 'id': id, 'generation': generation,
    #             'effect': effect, 'effect_short': effect_short,
    #             'pokemon': pokemon}
    #
    # def parse_stat(self):
    #     stat = self.json
    #     name = stat["name"]
    #     id = stat["id"]
    #     is_battle_only = stat["is_battle_only"]
    #     return {'name': name, 'id': id, "is_battle_only": is_battle_only}
    #
    # def parse_move(self, name):
    #     move = self.json
    #     name = name
    #     id = int(move['id']),
    #     generation = move['generation']['name'],
    #     accuracy = int(move['accuracy']),
    #     pp = int(move['pp']),
    #     power = int(move['power']),
    #     move_type = move['type']['name'],
    #     dmg_class = move['damage_class']['name'],
    #     effect_short = move['effect_entries'][0]['short_effect']
    #     return {'name': name, 'id': id, 'generation': generation,
    #             "accuracy": accuracy, "pp": pp, "power": power,
    #             "move_type": move_type, "dmg_class": dmg_class,
    #             'effect_short': effect_short}

