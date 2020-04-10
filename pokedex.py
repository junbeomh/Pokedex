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

    def __init__(self, mode: str, expanded: bool, input_data: str = None,
                 input_file: str = None, output_file: str = None):
        """
        Initializes a Request object.

        :param mode: a string, the mode ofe the intended request.
        :param expanded: a boolean, to indicate the request result's
                         data representation. True for extended, and
                         False for default mode.
        :param input_data: a string, data of the intended request.
        :param input_file: a string, the relative path of the file.
        :param output_file: a string, the name of the output file
                            that contains data of the request.
        """
        self.mode = mode
        self.expanded = expanded
        self.input_data = input_data
        self.input_file = input_file
        self.output_file = output_file

    def __str__(self):
        return f"Request: \n" \
               f"Mode: {self.mode}\n" \
               f"Expanded?: {self.expanded}\n" \
               f"Input Data: {self.input_data if not None else 'NA'}\n" \
               f"Input File: {self.input_file if not None else 'NA'}\n" \
               f"Output File: {self.output_file if not None else 'NA'}\n" \



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
    parser.add_argument("--expanded", type=str,
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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--inputfile", type=str,
                       help="Use this flag when providing a file. The file "
                            "must be an extension of type .txt")
    group.add_argument("--inputdata", type=str,
                       help="Use this flag when providing a data with either "
                            "name or id. The name must be a digit and id "
                            "must be a string.")
    return parser.parse_args()


class ReportGenerator:
    def __init__(self, request):
        self.request = request
        self.factory_mapping = {
            "pokemon": PokemonFactory,
            "ability": PokemonAbilityFactory,
            "move": PokemonMoveFactory
        }
        self.pokedexAPI = PokedexAPI()
        self.container = []

    def has_input_data(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        info = loop.run_until_complete(
            self.pokedexAPI.process_single_request(self.request.mode,
                                                   self.request.input_data))
        factory = self.factory_mapping[self.request.mode]([info],
                                                          self.request.expanded)
        for pokemon_object in factory.create():
            print(pokemon_object)
            self.container.append(pokemon_object)

    def generate_report(self):
        return self.has_input_data()


def main():
    args = setup_cmd_line_interface()
    request = Request(args.mode, args.expanded, args.inputdata, args.inputfile,
                      args.output)
    report = ReportGenerator(request)
    report.generate_report()


if __name__ == "__main__":
    main()
