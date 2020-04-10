from abc import ABC, abstractmethod
from pokemonretriever.pokedex_object import Pokemon, PokemonStat, PokemonMove


class PokemonObjectFactory(ABC):

    def __init__(self, data_set, is_expanded:bool=False):
        self.data_set = data_set
        self.is_expanded = is_expanded

    @abstractmethod
    def create(self):
        pass


class PokemonFactory(PokemonObjectFactory):

    def __init__(self, data, is_expanded:bool):
        super().__init__(data, is_expanded)

    def create_expanded_mode(self):
        pass

    def create_normal_mode(self):
        pass

    def create(self):
        if self.is_expanded:
            self.create_expanded_mode()
        else:
            self.create_normal_mode()


class PokemonStatFactory(PokemonObjectFactory):

    def __init__(self, data, is_expanded:bool):
        super().__init__(data, is_expanded)

    def create(self):
        for data in self.data_set:
            yield PokemonStat(**data)


class PokemonMoveFactory(PokemonObjectFactory):

    def __init__(self, data, is_expanded:bool):
        super().__init__(data, is_expanded)

    def create(self):
        for data in self.data_set:
            yield PokemonMove(**data)


def main():
    pass


if __name__ == "__main__":
    main()

