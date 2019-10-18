import math
from dataclasses import dataclass
from enum import Enum

from constants import *


class Direction(Enum):
    UP = 'up'
    RIGHT = 'right'
    DOWN = 'down'
    LEFT = 'left'

    @classmethod
    def get_by_self_tank(cls, tank):
        return {
            TANK_UP: Direction.UP,
            TANK_RIGHT: Direction.RIGHT,
            TANK_DOWN: Direction.DOWN,
            TANK_LEFT: Direction.LEFT
        }[tank]

    def get_delta(self):
        self_to_vec = {
            Direction.UP: [0, -1],
            Direction.RIGHT:[1, 0],
            Direction.DOWN:[0, 1],
            Direction.LEFT:[-1, 0],
        }
        return self_to_vec[self]


@dataclass
class Vec:
    x: int
    y: int
    dir: Direction


class Board:
    def __init__(self, text):
        self.text = text
        self.n = int(math.sqrt(len(text)))

        self.me = None
        for x in range(self.n):
            for y in range(self.n):
                ch = self.char(x, y)
                if ch in SELF_TANKS:
                    self.me = Vec(x, y, Direction.get_by_self_tank(ch))

    def char(self, x, y):
        return self.text[y * self.n + x]

    def get_view(self, vec, till_the_wall=False):
        x, y = vec.x, vec.y
        delta_x, delta_y = vec.dir.get_delta()
        res = ''
        while 0 <= x < self.n and 0 <= y < self.n:
            ch = self.char(x, y)
            res += ch
            x += delta_x
            y += delta_y
            if till_the_wall and ch in BARRIERS:
                break
        return res


