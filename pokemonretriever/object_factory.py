from abc import ABC, abstractmethod


class PokemonObjectFactory(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create(self):
        pass


class PokemonFactory(PokemonObjectFactory):

    def __init__(self):
        pass

    def create(self):
        pass


class PokemonStatFactory(PokemonObjectFactory):

    def __init__(self):
        pass

    def create(self):
        pass


class PokemonMoveFactory(PokemonObjectFactory):
    def __init__(self):
        pass

    def create(self):
        pass
