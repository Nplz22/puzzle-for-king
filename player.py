class Player:
    def __init__(self):
        self.inventory = []
        self.puzzles_cleared = 0
        self.name = "Hero"

    def add_item(self, item):
        self.inventory.append(item)

    def clear_puzzle(self):
        self.puzzles_cleared += 1
