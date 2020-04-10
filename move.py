class Move:

    def __init__(self, name: str, move_id: int, generation: str, accuracy: int,
                 pp: int, power: int, move_type: str, dmg_class: str,
                 effect_short: str):
        self.name = name
        self.id = move_id
        self.generation = generation
        self.accuracy = accuracy
        self.effect_short = effect_short
        self.pp = pp
        self.power = power
        self.move_type = move_type
        self.dmg_class = dmg_class

    def __str__(self):
        return f"Move: : {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Generation: {self.generation}\n" \
               f"Accuracy: {self.accuracy}\n" \
               f"PP: {self.pp}\n" \
               f"Power: {self.power}\n" \
               f"Type: {self.move_type}\n" \
               f"Damage class: {self.dmg_class}\n" \
               f"Effect: {self.effect_short}\n"
