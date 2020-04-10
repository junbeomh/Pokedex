class Stat:
    def __init__(self, name: str, id: int, is_battle_only: bool):
        self.name = name
        self.id = id
        self.is_battle_only = is_battle_only

    def __str__(self):
        return f"Stat: {self.name.title()}\n" \
               f"ID: {self.id}\n" \
               f"Is Battle Only: {self.is_battle_only}\n" \
