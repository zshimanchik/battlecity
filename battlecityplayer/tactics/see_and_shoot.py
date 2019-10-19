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

        enemies_dir_and_dist = self.get_enemies_dir_and_dist(board)

        if not enemies_dir_and_dist:
            return
        print('Enemy dists:', enemies_dir_and_dist)

        enemies_with_3d = [(player._estimate_action(dir.value), dist, dir) for dir, dist in enemies_dir_and_dist]
        player.visualizer.print('=====')
        for danger, dist, dir in enemies_with_3d:
            player.visualizer.print(f'enemy: {danger}, {dist}, {dir}')
        player.visualizer.print('=====')

        danger, dist, dir = min(enemies_with_3d, key=lambda x: (x[0], x[1]))
        self.action = 'act,' + dir.value
        # if danger > 1:
        #     self.usability = 0.001
        if dist < 6:
            self.usability = 0.9
        else:
            self.usability = 0.8

    def get_enemies_dir_and_dist(self, board):
        enemies_dir_and_dist = []
        for dir in Direction:
            view = board.get_view(Vec(board.me.pos, dir))
            for i, ch in enumerate(view):
                if ch in ENEMIES:
                    enemies_dir_and_dist.append((dir, i))
        return enemies_dir_and_dist
