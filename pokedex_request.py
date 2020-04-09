"""
This module depicts the use of a making a HTTP GET requests to retrieve
information about pokemons.
"""

# John (JunBeom) Han
# A01064824
# 2020/04/03

import aiohttp
import asyncio
import ssl


class PokedexAPI:
    """
    A class for making HTTP GET request to retrieve data about
    pokemon objects.
    """

    def __init__(self):
        """
        Initializes a PokedexAPI object.

        attributes:
            url: a string, the url to make api request with parameters.
            session: an aiohttp Client HTTP session.
        """
        self.url = "https://pokeapi.co/api/v2/{}/{}"
        self.session = aiohttp.ClientSession

    @staticmethod
    async def get_pokedex_data(url: str, session: aiohttp.ClientSession):
        """
        Retrieves pokemon data through the execution of GET http
        requests.

        :param url: a string, the url to make api request with parameters.
        :param session: an aiohttp Client HTTP session.
        :return: a dict, json representation of GET http response.
        """
        response = await session.request(method="GET", url=url,
                                         ssl=ssl.SSLContext())
        json_response = await response.json()
        return json_response

    async def process_single_request(self, req_type: str, req_id: str):
        """
        Executes a single HTTP GET request to retrieve pokemon data.

        :param req_type: a string, the category type to request.
        :param req_id: a string, the id or name of pokemon.
        :return: a dict, json representation of GET http response.
        """
        request_url = self.url.format(req_type, req_id)
        async with self.session() as session:
            response = await self.get_pokedex_data(request_url, session)
            return response

    async def process_requests(self, req_type: str, requests: list):
        """
        Executes multiple HTTP GET requests to retrieve pokemon data.

        :param req_type: a string, the category type to request.
        :param requests: a list of strings, a list of pokemon id or
                         names.
        :return: a dict, json representation of GET http response.
        """
        async with self.session() as session:
            list_urls = [self.url.format(req_type, req_id) for
                         req_id in requests]
            coroutines = [self.get_pokedex_data(url, session) for url in
                          list_urls]
            responses = await asyncio.gather(*coroutines)
            return responses


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



def main():
    pokedex = PokedexAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    requests = ["charmander", "squirtle", "bulbasaur", "pikachu", "151"]
    pokemons = loop.run_until_complete(pokedex.process_requests("pokemon",
                                                                requests))

    pokemon_list = [Pokemon(pokemon['id'], pokemon['name'], pokemon['height'],
                            pokemon['weight'], pokemon['types'],
                            pokemon['stats'], pokemon['abilities'],
                            pokemon['moves'])
                    for pokemon in pokemons]

    for pokemon in pokemon_list:
        print(pokemon)


if __name__ == "__main__":
    main()
