"""
"""

import argparse
from enum import Enum
from pokemonretriever.pokedex_object_factory import PokemonFactory, \
    PokemonMoveFactory, PokemonAbilityFactory
from pokemonretriever.pokedex_request import PokedexAPI
import asyncio


class PokedexMode(Enum):
    POKEMON = "pokemon"
    ABILITY = "ability"
    MOVE = "move"


class Request:

    """
    A request object represents a request specifications about
    the program.
    """

    def __init__(self, mode: str, expanded: bool = False, 
                 input_data: str = None, input_file: str = None, 
                 output_file: str = None):
        """
        Initializes a Request object.

        :param mode: a string, the mode of the intended request.
        :param expanded: a boolean, to indicate the request result's
                         data representation. True for extended, and
                         False for default mode.
        :param input_data: a string, data of the intended request.
        :param input_file: a string, the relative path of the file.
        :param output_file: a string, the name of the output file
                            that contains data of the request.
        """
        if ".txt" not in input_file:
            raise Exception("File extension must be .txt")
        self.mode = mode
        self.expanded = expanded if expanded is not None else False
        self.input_data = [input_data]
        self.input_file = input_file
        if input_file:
            self.__process_file_to_data()
        self.output_file = output_file
        self.api = PokedexAPI()

    def __process_file_to_data(self):
        try:
            with open(file=self.input_file, mode='r', encoding='UTF-8') as f:
                self.input_data = [line.rstrip('\n').lower() for line in f]
        except OSError as e:
            raise FileNotFoundError(e)

    def process_request(self) -> list:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        info = loop.run_until_complete(
            self.api.process_requests(self.mode, self.input_data))
        return info

    def __str__(self):
        return f"Request: \n" \
               f"Mode: {self.mode}\n" \
               f"Expanded?: {self.expanded}\n" \
               f"Input Data: {self.input_data if not None else 'NA'}\n" \
               f"Input File: {self.input_file if not None else 'NA'}\n" \
               f"Output File: {self.output_file if not None else 'NA'}\n"


class Pokedex:

    """ """
    factory_map = {
        PokedexMode.POKEMON: PokemonFactory,
        PokedexMode.ABILITY: PokemonAbilityFactory,
        PokedexMode.MOVE: PokemonMoveFactory
    }

    def __init__(self, request):
        self.request = request
        self.factory = self.factory_map[PokedexMode(self.request.mode)]
        self.container = []

    def get_pokemon_objects(self):
        info = self.request.process_request()
        factory = self.factory(info, is_expanded=self.request.expanded)
        for pokemon_object in factory.create():
            print(pokemon_object)
            self.container.append(pokemon_object)

    def generate_report(self):
        self.get_pokemon_objects()
        if self.request.output_file is None:
            output_file = "output.txt"
        else:
            output_file = self.request.output_file
        with open(file=output_file, mode="w+", encoding="UTF-8") as file:
            for objects in self.container:
                file.write(str(objects))


def setup_cmd_line_interface():
    """
    Sets up a command-line interface to accept the user's specification
    about the program mode and optional program arguments.

    :return: the namespace containing the arguments to the program command.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str,
                        choices=['pokemon', 'move', 'ability'],
                        help="Choose one of the three values to perform"
                             "query.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--inputfile", type=str,
                       help="Use this flag when providing a file. The file "
                            "must be an extension of type .txt")
    group.add_argument("--inputdata", type=str,
                       help="Use this flag when providing a data with either "
                            "name or id. The name must be a digit and id "
                            "must be a string.")
    parser.add_argument("--expanded", action="store_true",
                        help="Use this flag if you wish to perform sub-queries"
                             "to get more information about particular "
                             "attributes. Only supported for mode type "
                             "'pokemon'.")
    parser.add_argument("--output", type=str,
                        help="Use this flag if you want the query results "
                             "to be outputted into a new file. The file"
                             "must be an extension of type .txt. If not "
                             "specified, the results will be printed on the "
                             "console.")
    return parser.parse_args()


def main():
    try:
        args = setup_cmd_line_interface()
        request = Request(args.mode, args.expanded, args.inputdata, 
                          args.inputfile, args.output)
        pokedex = Pokedex(request)
        pokedex.generate_report()
    except Exception as e:
        print("Error: " + str(e))
    except FileNotFoundError as fe:
        print(str(fe))


if __name__ == "__main__":
    main()
