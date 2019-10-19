from models import Direction, Vec
from tactics import Tactics
from constants import *


class DodgeBullet(Tactics):
    def update(self, player):
        self.action = ''
        self.usability = 0
        if player.fire_countdown == 0:
            return
        self.usability = 0.2
        board = player.board
        potenial_poss = [player.board.me.pos]
        for dir in Direction:
            neighbour = board.me.pos + dir.get_delta()
            if board.is_belong(neighbour) and board.char(neighbour.x, neighbour.y) not in BARRIERS:
                potenial_poss.append(neighbour)

        potenial_poss_with_danger = [(pos, self._analyze_pos(board, pos)) for pos in potenial_poss]
        for pos, danger in potenial_poss_with_danger:
            player.visualizer.client.set_pen(int((danger / 1) * 255), 0, 0)
            player.visualizer.client.draw_rect(pos.x, pos.y)
            if pos == player.board.me.pos:
                dir = 'STAY'
            else:
                dir = (pos - player.board.me.pos).give_direction().value
            player.visualizer.print(f"{dir} danger={danger}")

        chosen_pos = min(potenial_poss, key=lambda pos: self._analyze_pos(board, pos))
        if chosen_pos == board.me.pos:
            self.action = ''
        else:
            delta = chosen_pos-player.board.me.pos
            print('delta:', delta)
            self.action = delta.give_direction().value

    def _analyze_pos(self, board, pos):
        danger = 0
        for dir in Direction:
            view = board.get_view(Vec(pos, dir))
            for dist, ch in enumerate(view):
                if ch == BULLET and dist <= 3:
                    danger += 1
                if ch in OTHER_TANKS and dist <= 3:
                    danger += 1
        return danger
