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
            Direction.UP: Point(0, -1),
            Direction.RIGHT: Point(1, 0),
            Direction.DOWN: Point(0, 1),
            Direction.LEFT: Point(-1, 0),
        }
        return self_to_vec[self]


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        else:
            raise ValueError()

    def __sub__(self, other):
        if isinstance(other, Point):
            return Point(self.x - other.x, self.y - other.y)
        else:
            raise ValueError()

    def length(self):
        return math.hypot(self.x, self.y)

    def get_neighbours(self):
        for dir in Direction:
            yield self + dir.get_delta()

    def give_direction(self):
        if self.x == 0 and self.y < 0:
            return Direction.UP
        elif self.x == 0 and self.y > 0:
            return Direction.DOWN
        elif self.y == 0 and self.x > 0:
            return Direction.RIGHT
        elif self.y == 0 and self.x < 0:
            return Direction.LEFT
        else:
            raise ValueError()


@dataclass
class Vec:
    pos: Point
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
                    self.me = Vec(Point(x, y), Direction.get_by_self_tank(ch))

    def char(self, x, y):
        return self.text[y * self.n + x]

    def get_view(self, vec, till_the_wall=True):
        cur_pos = vec.pos
        delta = vec.dir.get_delta()
        res = ''
        while 0 <= cur_pos.x < self.n and 0 <= cur_pos.y < self.n:
            ch = self.char(cur_pos.x, cur_pos.y)
            res += ch
            cur_pos += delta
            if till_the_wall and ch in BARRIERS:
                break
        return res

    def is_belong(self, point):
        return 0 <= point.x < self.n and 0 <= point.y < self.n

    def get_all_enemies(self):
        for x in range(self.n):
            for y in range(self.n):
                if self.char(x, y) in ENEMIES:
                    yield Point(x, y)
