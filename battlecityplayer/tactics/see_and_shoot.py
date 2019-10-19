from models import Direction, Vec
from tactics import Tactics

from constants import *


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
            view = board.get_view(Vec(me.pos, dir), True)
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
            self.usability = 0.8
