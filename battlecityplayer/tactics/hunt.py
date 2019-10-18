from collections import deque

from models import Direction
from tactics import Tactics
from constants import *


class Hunt(Tactics):
    def update(self, player):
        self.usability = 0
        self.action = ''
        board = player.board
        path = self.find_path_to_enemy(board)
        if path and len(path) > 3:
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
