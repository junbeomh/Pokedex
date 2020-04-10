"""
"""


import aiohttp
import asyncio
import ssl

from pokemonretriever.pokedex_object import Pokemon, PokemonAbility, \
    PokemonStat, PokemonMove


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
        if len(requests) == 1:
            return await self.process_single_request(req_type, requests[0])
        async with self.session() as session:
            list_urls = [self.url.format(req_type, req_id) for
                         req_id in requests]
            coroutines = [self.get_pokedex_data(url, session) for url in
                          list_urls]
            responses = await asyncio.gather(*coroutines)
            return responses


def main():
    pokedex = PokedexAPI()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    requests = ["charmander", "squirtle", "bulbasaur", "pikachu", "151"]
    pokemons = loop.run_until_complete(pokedex.process_requests("pokemon",
                                                                requests))

    pokemon_list = [Pokemon(pokemon['name'],
                            int(pokemon['id']),
                            int(pokemon['height']),
                            int(pokemon['weight']),
                            pokemon['types'],
                            pokemon['stats'],
                            pokemon['abilities'],
                            pokemon['moves'])
                    for pokemon in pokemons]

    for pokemon in pokemon_list:
        print(pokemon)

    requests = ["1", "cut", "ice-punch"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    moves = loop.run_until_complete(pokedex.process_requests("move", requests))
    move_list = [PokemonMove(move['name'],
                             int(move['id']),
                             move['generation']['name'],
                             int(move['accuracy']),
                             int(move['pp']),
                             int(move['power']),
                             move['type']['name'],
                             move['damage_class']['name'],
                             move['effect_entries'][0]['short_effect'])
                 for move in moves]
    for move in move_list:
        print(move)

    requests = ["1", "sturdy", "levitate"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    abilities = loop.run_until_complete(pokedex.process_requests("ability",
                                                                 requests))
    ability_list = [PokemonAbility(ability["name"], int(ability["id"]),
                                   ability["generation"]["name"],
                                   ability["effect_entries"][0]["effect"],
                                   ability["effect_entries"][0]["short_effect"],
                                   ability["pokemon"])
                    for ability in abilities]
    for ability in ability_list:
        print(ability)

    requests = ["speed", "defense", "hp"]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    stats = loop.run_until_complete(pokedex.process_requests("stat", requests))
    stat_list = [PokemonStat(stat["name"], stat["id"], stat["is_battle_only"])
                 for stat in stats]
    for stat in stat_list:
        print(stat)




if __name__ == "__main__":
    main()
