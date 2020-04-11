"""
Contains class definitions for the API.
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
    async def __get_pokedex_data(url: str, session: aiohttp.ClientSession):
        """
        Retrieves pokemon data through the execution of GET http
        requests.

        :param url: a string, the url to make api request with parameters.
        :param session: an aiohttp Client HTTP session.
        :return: a list, json representation of GET http response.
        """
        response = await session.request(method="GET", url=url,
                                         ssl=ssl.SSLContext())
        json_response = await response.json()
        return json_response

    async def __process_single_request(self, req_type: str, req_id: str):
        """
        Executes a single HTTP GET request to retrieve pokemon data.

        :param req_type: a string, the category type to request.
        :param req_id: a string, the id or name of pokemon.
        :return: a list, json representation of GET http response.
        """
        request_url = self.url.format(req_type, req_id)
        async with self.session() as session:
            response = await self.__get_pokedex_data(request_url, session)
            return response

    async def process_requests(self, req_type: str, requests: list):
        """
        Executes multiple HTTP GET requests to retrieve pokemon data.

        :param req_type: a string, the category type to request.
        :param requests: a list of strings, a list of pokemon id or
                         names.
        :return: a list, json representation of GET http response.
        """
        if isinstance(requests, str):
            return await self.__process_single_request(req_type, requests[0])
        else:
            async with self.session() as session:
                list_urls = [self.url.format(req_type, req_id) for
                             req_id in requests]
                coroutines = [self.__get_pokedex_data(url, session) for url in
                              list_urls]
                responses = await asyncio.gather(*coroutines)
                return responses
