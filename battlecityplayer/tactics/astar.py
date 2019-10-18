from collections import deque

from models import Point, Direction
from tactics import Tactics
from constants import *


class AStar(Tactics):
    def update(self, player):
        self.usability = 0
        self.action = ''
        board = player.board
        path = self.find_path_to_enemy(board, Point(20, 5))
        if path and len(path) > 1:
            print(path)
            delta = path[1] - player.board.me.pos
            print(f'delta: {path[1]} - {player.board.me.pos} = {delta}')
            print('dir: ', delta.give_direction())
            self.action = delta.give_direction().value
            self.usability = 1

    def h(self, start, target):
        return (target - start).length()


    def find_path_to_enemy(self, board, target):
        INF = 999999
        g_dist_mtrx = [[INF] * board.n for _ in range(board.n)]
        f_dist_mtrx = [[INF] * board.n for _ in range(board.n)]
        visited = set()
        queue = deque()
        queue.appendleft(board.me.pos)
        g_dist_mtrx[board.me.pos.x][board.me.pos.y] = 0
        f_dist_mtrx[board.me.pos.x][board.me.pos.y] = self.h(board.me.pos, target)

        while queue:
            cur_pos = min(queue, key=lambda cur: f_dist_mtrx[cur.x][cur.y])
            if cur_pos == target:
                return self._restore_path(cur_pos, g_dist_mtrx)

            queue.remove(cur_pos)
            visited.add(cur_pos)

            for dir in Direction:
                next_pos = cur_pos + dir.get_delta()
                if next_pos not in visited and 0 <= next_pos.x < board.n and 0 <= next_pos.y < board.n:
                    ch = board.char(next_pos.x, next_pos.y)
                    if ch == WALL:
                        visited.add(next_pos)
                        continue
                    dist_to_next = g_dist_mtrx[cur_pos.x][cur_pos.y] + 1 # todo consider wall
                    if dist_to_next < g_dist_mtrx[next_pos.x][next_pos.y]:
                        g_dist_mtrx[next_pos.x][next_pos.y] = dist_to_next
                        f_dist_mtrx[next_pos.x][next_pos.y] = dist_to_next + self.h(next_pos, target)
                        if next_pos not in queue:
                            queue.append(next_pos)

    def _restore_path(self, cur_pos, dist_mtrx):
        path = deque()
        path.appendleft(cur_pos)
        cur_dist = dist_mtrx[cur_pos.x][cur_pos.y]
        while cur_dist > 0:
            best_dist = 99999999
            best_next_pos = None
            for dir in Direction:
                next_pos = cur_pos + dir.get_delta()
                if 0 <= next_pos.x < len(dist_mtrx) and 0 <= next_pos.y < len(dist_mtrx):
                    if dist_mtrx[next_pos.x][next_pos.y] < best_dist:
                        best_dist = dist_mtrx[next_pos.x][next_pos.y]
                        best_next_pos = next_pos
            path.appendleft(best_next_pos)
            cur_pos = best_next_pos
            cur_dist = best_dist
        return path
