import random
from collections import deque

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
            self.usability = 0.7


class Hunt(Tactics):
    def update(self, player):
        self.usability = 0
        self.action = ''
        board = player.board
        path = self.find_path_to_enemy(board)
        if len(path) > 3:
            print(path)
            delta = path[1] - player.board.me.pos
            print('delta: ', delta)
            print('dir: ', delta.give_direction())
            self.action = delta.give_direction().value
            self.usability = 0.7

    def find_path_to_enemy(self, board):
        dist_mtrx = [[0] * board.n for _ in range(board.n)]  # 0 - means unvisited
        queue = deque()
        queue.appendleft(board.me.pos)
        dist_mtrx[board.me.pos.x][board.me.pos.y] = 1
        while queue:
            cur_pos = queue.pop()
            cur_distance = dist_mtrx[cur_pos.x][cur_pos.y]
            for dir in Direction:
                next_pos = cur_pos + dir.get_delta()
                if 0 <= next_pos.x < board.n and 0 <= next_pos.y < board.n:
                    ch = board.char(next_pos.x, next_pos.y)
                    if ch in ENEMIES:
                        dist_mtrx[next_pos.x][next_pos.y] = cur_distance + 1
                        return self._restore_path(next_pos, dist_mtrx)
                    if ch not in BARRIERS and dist_mtrx[next_pos.x][next_pos.y] == 0:
                        dist_mtrx[next_pos.x][next_pos.y] = cur_distance + 1
                        queue.appendleft(next_pos)

    def _restore_path(self, cur_pos, dist_mtrx):
        path = deque()
        path.appendleft(cur_pos)
        cur_dist = dist_mtrx[cur_pos.x][cur_pos.y]
        while cur_dist > 1:
            for dir in Direction:
                next_pos = cur_pos + dir.get_delta()
                if 0 <= next_pos.x < len(dist_mtrx) and 0 <= next_pos.y < len(dist_mtrx):
                    if dist_mtrx[next_pos.x][next_pos.y] == cur_dist - 1:
                        path.appendleft(next_pos)
                        cur_pos = next_pos
                        cur_dist -= 1
                        break
        return path


class DodgeBullet(Tactics):
    def update(self, player):
        self.action = ''
        self.usability = 0
