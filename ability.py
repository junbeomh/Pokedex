class Ability:
    def __init__(self, name: str, id: int, generation: str, effect: str,
                 effect_short: str, pokemons: list):
        self.name = name
        self.id = id
        self.generation = generation
        self.effect = effect
        self.effect_short = effect_short
        self.pokemon = self.parse_pokemon(pokemons)

    @staticmethod
    def parse_pokemon(pokemons: list):
        pokemon_list = []
        for pokemon in pokemons:
            pokemon_list.append(pokemon["pokemon"]["name"])
        return pokemon_list

    def __str__(self):
        return f"Ability: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Generation: {self.generation}\n" \
               f"Effect: {self.effect}\n" \
               f"Short Effect: {self.effect_short}\n" \
               f"Pokemon: {self.pokemon}\n" \
