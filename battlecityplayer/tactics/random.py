import random

from tactics import Tactics


class RandomTactics(Tactics):
    def __init__(self):
        super().__init__()
        self.usability = 0.01

    def update(self, player):
        move = random.choice(['up', 'right', 'down', 'left'])
        self.action = move
