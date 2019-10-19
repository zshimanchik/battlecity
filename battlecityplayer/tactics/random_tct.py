import random

from constants import BARRIERS
from models import Direction
from tactics import Tactics


class RandomTactics(Tactics):
    def __init__(self):
        super().__init__()
        self.usability = 0.01

    def update(self, player):
        board = player.board
        free_directions = []
        for dir in Direction:
            neighbour = board.me.pos + dir.get_delta()
            if board.is_belong(neighbour) and board.char(neighbour.x, neighbour.y) not in BARRIERS:
                free_directions.append(dir)
        if free_directions:
            chosen_direction = random.choice(free_directions)
            self.action = chosen_direction.value
        else:
            self.action = ''
