from collections import deque

import player
from constants import *
from models import Point, Direction
from tactics import Tactics


class AStar(Tactics):
    def update(self, player):
        self.usability = 0.0
        self.action = ''
        board = player.board
        enemies = board.get_all_enemies()

        path = self.find_path_to_enemy(board, Point(17, 32), player)
        if path and len(path) > 1:
            print(path)
            delta = path[1] - player.board.me.pos
            print(f'delta: {path[1]} - {player.board.me.pos} = {delta}')
            print('dir: ', delta.give_direction())
            self._draw_path(path, player.visualizer)
            ch = board.char(path[1].x, path[1].y)
            self.action = delta.give_direction().value
            if ch in CONSTRUCTIONS:
                self.action += ',act'
            self.usability = 0.0

    def _draw_path(self, path, visualizer):
        if len(path) > 1:
            ipath = iter(path)
            p1 = next(ipath)
            for p2 in ipath:
                visualizer.client.draw_line(p1.x, p1.y, p2.x, p2.y)
                p1 = p2

    def h(self, start, target):
        return (target - start).length()

    def find_path_to_enemy(self, board, target, player):
        INF = 999999
        actual_dist_mtrx = [[INF] * board.n for _ in range(board.n)]
        potential_dist_mtrx = [[INF] * board.n for _ in range(board.n)]
        came_from_mtrx = [[None] * board.n for _ in range(board.n)]
        visited = set()
        queue = deque()
        queue.appendleft(board.me.pos)
        actual_dist_mtrx[board.me.pos.x][board.me.pos.y] = 0
        potential_dist_mtrx[board.me.pos.x][board.me.pos.y] = self.h(board.me.pos, target)

        while queue:
            cur_pos = queue.pop()
            # cur_pos = min(queue, key=lambda cur: potential_dist_mtrx[cur.x][cur.y])
            # if cur_pos == target:
            #     return self._restore_path(cur_pos, actual_dist_mtrx)

            # queue.remove(cur_pos)
            visited.add(cur_pos)

            for dir in Direction:
                next_pos = cur_pos + dir.get_delta()
                if next_pos not in visited and board.is_belong(next_pos):
                    ch = board.char(next_pos.x, next_pos.y)
                    if ch == WALL:
                        visited.add(next_pos)
                        continue
                    dist_to_next = actual_dist_mtrx[cur_pos.x][cur_pos.y] + self._d(ch)
                    if dist_to_next < actual_dist_mtrx[next_pos.x][next_pos.y]:
                        actual_dist_mtrx[next_pos.x][next_pos.y] = dist_to_next
                        potential_dist_mtrx[next_pos.x][next_pos.y] = dist_to_next + self.h(next_pos, target)
                        came_from_mtrx[next_pos.x][next_pos.y] = cur_pos
                        if next_pos not in queue:
                            queue.appendleft(next_pos)
        # self.draw(player.visualizer, actual_dist_mtrx, came_from_mtrx)
        return self._restore_path(target, actual_dist_mtrx)

    def draw(self, visualizer, actual_dist_mtrx, came_from_mtrx):
        for x in range(len(actual_dist_mtrx)):
            for y in range(len(actual_dist_mtrx[0])):
                # visualizer.client.draw_text(x, y, str(actual_dist_mtrx[x][y]))
                if came_from_mtrx[x][y] is not None:
                    print(f"p={Point(x,y)} came_from={came_from_mtrx[x][y]} diff={Point(x, y) - came_from_mtrx[x][y]}")
                    # print(f"{}")
                    arrow = (came_from_mtrx[x][y] - Point(x, y)).get_direction().get_ascii_arrow()
                    visualizer.client.draw_text(x, y, arrow)

    def _d(self, ch):
        if ch in CONSTRUCTIONS:
            return SHOTS_TO_DESTROY[ch] * player.Player.FIRE_COUNTDOWN
        return 1

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
