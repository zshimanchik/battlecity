from collections import deque

import player
from constants import *
from models import Point, Direction
from tactics import Tactics


class AStarHunt(Tactics):
    def update(self, player):
        self.usability = 0.0
        self.action = ''
        board = player.board
        self.calculate_matrixes(board)

        # self.draw_came_from_mtrx(player.visualizer)
        # self.draw_dist_mtrx(player.visualizer)

        closest_enemy = min(board.get_all_enemies(), key=lambda enemy: self.dist_mtrx[enemy.x][enemy.y])
        path = self._restore_path(closest_enemy, player.board.me.pos)
        if path and len(path) > 4:
            print(path)
            delta = path[1] - player.board.me.pos
            print(f'delta: {path[1]} - {player.board.me.pos} = {delta}')
            print('dir: ', delta.give_direction())
            self._draw_path(path, player.visualizer)
            ch = board.char(path[1].x, path[1].y)
            self.action = delta.give_direction().value
            if ch in CONSTRUCTIONS or ch in ENEMIES:
                self.action += ',act'

            danger = player._estimate_pos(path[1])
            if danger >= 1:
                self.usability = 0
            else:
                self.usability = 0.5

    def _draw_path(self, path, visualizer):
        if len(path) > 1:
            ipath = iter(path)
            p1 = next(ipath)
            for p2 in ipath:
                visualizer.client.draw_line(p1.x, p1.y, p2.x, p2.y, color=[255,0,0])
                p1 = p2

    def calculate_matrixes(self, board):
        INF = 999999
        dist_mtrx = [[INF] * board.n for _ in range(board.n)]
        came_from_mtrx = [[None] * board.n for _ in range(board.n)]
        visited = set()
        queue = deque()
        queue.appendleft(board.me.pos)
        dist_mtrx[board.me.pos.x][board.me.pos.y] = 0

        while queue:
            cur_pos = min(queue, key=lambda pos: dist_mtrx[pos.x][pos.y])
            queue.remove(cur_pos)
            visited.add(cur_pos)

            for dir in Direction:
                next_pos = cur_pos + dir.get_delta()
                if next_pos not in visited and board.is_belong(next_pos):
                    ch = board.char(next_pos.x, next_pos.y)
                    if ch == WALL:
                        visited.add(next_pos)
                        continue
                    dist_to_next = dist_mtrx[cur_pos.x][cur_pos.y] + self._d(ch)
                    if dist_to_next < dist_mtrx[next_pos.x][next_pos.y]:
                        dist_mtrx[next_pos.x][next_pos.y] = dist_to_next
                        came_from_mtrx[next_pos.x][next_pos.y] = cur_pos
                        if next_pos not in queue:
                            queue.appendleft(next_pos)
        self.dist_mtrx = dist_mtrx
        self.came_from_mtrx = came_from_mtrx

    def draw_dist_mtrx(self, visualizer):
        for x in range(len(self.dist_mtrx)):
            for y in range(len(self.dist_mtrx[0])):
                visualizer.client.draw_text(x, y, str(self.dist_mtrx[x][y]))

    def draw_came_from_mtrx(self, visualizer):
        came_from_mtrx = self.came_from_mtrx
        for x in range(len(came_from_mtrx)):
            for y in range(len(came_from_mtrx[0])):
                if came_from_mtrx[x][y] is not None:
                    arrow = (Point(x, y) - came_from_mtrx[x][y]).get_direction().get_ascii_arrow()
                    visualizer.client.draw_text(x, y, arrow)

    def _d(self, ch):
        if ch in CONSTRUCTIONS:
            return SHOTS_TO_DESTROY[ch] * (player.Player.FIRE_COUNTDOWN + 1) + 1 # (fire_countdown + 1 move) + 1 for dangerous
        return 1

    def _restore_path(self, cur_pos, my_pos):
        path = deque()
        while cur_pos != my_pos and cur_pos is not None:
            path.appendleft(cur_pos)
            cur_pos = self.came_from_mtrx[cur_pos.x][cur_pos.y]

        if cur_pos is not None:
            path.appendleft(cur_pos)
        return path
