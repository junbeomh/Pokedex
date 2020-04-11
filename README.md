# COMP3522_Assignment3

John(JunBeom) Han: A01064824, Joshua Lam: A00959199

Use case:
 - normal mode: 
    - file: python3 pokedex.py pokemon --inputfile "input.txt"
    - data: python3 pokedex.py move --inputdata "1"
 - expanded mode:
    - file: python3 pokedex.py pokemon --inputfile "input.txt" --expanded
    - data: python3 pokedex.py pokemon --inputdata "1" --expanded

Our pokedex application has five modules:
 - pokedex.py
 - pokedex_object.py
 - pokedex_object_factory.py
 - pokedex_parser.py
 - pokedex-request.py 
 
Pokedex.py
 - This module is responsible for handling client side code. We handle the
 terminal input commands, file I/O and factory calls.
    
Pokedex_object.py
  - We implement our PokedexObject ABC class and its 4 child classes in this
  module: Pokemon, PokemonAbility, PokemonMove, and PokemonStat. Here we store
  all the information for each respective PokedexObject and format how each
  child class is displayed when printed.
  
Pokedex_object_factory.py
 - This is our factory module responsible for instantiating our PokedexObjects.
 There is a corresponding factory for each class in the pokedex_object.py 
 module.
 
Pokedex_parser.py
 - This module takes the information grabbed by the http request and removes
 any extra data that we do not use from the API. This modified data is then 
 used by the factory classes to instantiate the PokedexObjects.
 
Pokedex_request.py
 - The information taken from the terminal commands is used in this module to 
 make the appropriate HTTP requests. 
 

 
 
