import random

from constants import *
from models import Vec, Direction


class Tactics:
    def __init__(self):
        self.usability = 0.5
        self.action = ''

    def update(self, player):
        pass


class RandomTactics(Tactics):
    def __init__(self):
        super().__init__()
        self.usability = 0.01

    def update(self, player):
        move = random.choice(['up', 'right', 'down', 'left'])
        self.action = move


class SeeAndShoot(Tactics):
    def update(self, player):
        self.action = ''
        self.usability = 0
        if player.fire_countdown != 0:
            return
        board = player.board
        me = board.me
        enemies_dir_and_dist = []
        for dir in Direction:
            view = board.get_view(Vec(me.x, me.y, dir), True)
            print(f'{dir} {view!r}')
            for i, ch in enumerate(view):
                if ch in ENEMIES:
                    enemies_dir_and_dist.append((dir, i))
        if not enemies_dir_and_dist:
            return
        print('Enemy dists:', enemies_dir_and_dist)
        enemy_dir, enemy_dist = min(enemies_dir_and_dist, key=lambda x: x[1])
        self.action = 'act,' + enemy_dir.value
        if enemy_dist < 6:
            self.usability = 0.9
        else:
            self.usability = 0.7


class DodgeBullet(Tactics):
    def update(self, player):
        self.action = ''
        self.usability = 0
