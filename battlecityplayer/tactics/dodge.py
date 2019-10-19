import random

from models import Direction, Vec
from tactics import Tactics
from constants import *


class DodgeBullet(Tactics):
    def update(self, player):
        self.action = ''
        self.usability = 0

        board = player.board
        potenial_poss = [player.board.me.pos]
        for dir in Direction:
            neighbour = board.me.pos + dir.get_delta()
            if board.is_belong(neighbour) and board.char(neighbour.x, neighbour.y) not in BARRIERS:
                potenial_poss.append(neighbour)

        self.visualize(player, potenial_poss)
        # potential_poss_with_danger = [(p, player._estimate_pos(p)) for p in potenial_poss]
        # filtered_potenial_poss = [pos for pos, danger in potential_poss_with_danger if danger <= 1]
        # min_danger = min(danger for pos, danger in potential_poss_with_danger)
        # filtered_potenial_poss = [pos for pos, danger in potential_poss_with_danger if danger == min_danger]
        # chosen_pos = random.choice(filtered_potenial_poss)
        chosen_pos = min(potenial_poss, key=lambda pos: player._estimate_pos(pos))
        if chosen_pos == board.me.pos:
            self.action = ''
        else:
            delta = chosen_pos-player.board.me.pos
            print('delta:', delta)
            self.action = delta.give_direction().value

        if player.fire_countdown == 0:
            self.usability = 0.001
        else:
            self.usability = 0.2

    def visualize(self, player, potenial_poss):
        potenial_poss_with_danger = [(pos, player._estimate_pos(pos)) for pos in potenial_poss]
        for pos, danger in potenial_poss_with_danger:
            player.visualizer.client.set_pen(int((danger / 2) * 255), 0, 0)
            player.visualizer.client.draw_rect(pos.x, pos.y)
            if pos == player.board.me.pos:
                dir = 'STAY'
            else:
                dir = (pos - player.board.me.pos).give_direction().value
            player.visualizer.print(f"{dir} danger={danger}")
