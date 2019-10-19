import logging
import math
from collections import deque

from models import Board, Direction, Vec, Point
from tactics.astarhunt import AStarHunt
from tactics.dodge import DodgeBullet
from tactics.hunt import Hunt
from tactics.random_tct import RandomTactics
from tactics.see_and_shoot import SeeAndShoot
from constants import *

logger = logging.getLogger(__name__)


class Player:
    tactics = [
        AStarHunt(),
        RandomTactics(),
        SeeAndShoot(),
        # Hunt(),
        DodgeBullet(),
    ]

    FIRE_COUNTDOWN = 4
    SAVE_HISTORY = True

    def __init__(self, visualizer):
        self.board = None
        self.visualizer = visualizer
        self.history = deque(maxlen=3)
        self.fire_countdown = 0
        self.result = ''

    def turn(self, board):
        try:
            self.save_history(board)
            result = self._turn(board)
            self.result = result
            print(f'result: {result}')
            self.visualizer.print(f'result: {result}')
            self.visualizer.update(self)
        except Exception as ex:
            print('There is an exception')
            logger.exception('There is some exception', exc_info=ex)
            result = ''
        return result

    def _turn(self, board):
        self.board = Board(board)
        self.history.appendleft(board)
        self.tick()

        for row in range(self.board.n):
            print(self.board.text[self.board.n*row:self.board.n*(row+1)])

        if self.board.me is None:
            self.reset()
            print("Dead. Do nothing")
            return ''

        self.visualizer.print(f'fc={self.fire_countdown}')
        for tactic in self.tactics:
            tactic.update(self)


        possible_actions = [tactic.action for tactic in self.tactics]
        action_dangerous = [self._estimate_action(action) for action in possible_actions]
        self.visualizer.print(
            '\n'.join('{t.__class__.__name__:<14} {t.usability:.2f} {t.action} {d}'.format(t=t,d=d)
                      for t,d in zip(self.tactics, action_dangerous)))



        current_tactics = max(self.tactics, key=lambda t: t.usability)
        action = current_tactics.action
        if 'act' in action:
            self.fire_countdown = self.FIRE_COUNTDOWN
        assert isinstance(action, str)
        # return 'right,act'
        return action

    def reset(self):
        self.fire_countdown = 0

    def tick(self):
        if self.fire_countdown > 0:
            self.fire_countdown -= 1

    def _estimate_action(self, action):
        action = action.replace('act', '').replace(',', '')
        if action == '':
            pos = self.board.me.pos
        else:
            dir = Direction(action)
            pos = self.board.me.pos + dir.get_delta()
        return self._estimate_pos(pos)

    def _estimate_pos(self, pos):
        danger = 0
        for dir in Direction:
            view = self.board.get_view(Vec(pos, dir))
            for dist, ch in enumerate(view):
                if ch == BULLET and dist <= 2:
                    if ((dist == 0 and self.is_my_bullet(pos))  # my bullet in front of me
                            or (dist == 2 and self.is_my_bullet(pos + dir.get_delta() * dist))):  # my bullet from the back
                        pass
                    else:
                        danger += 1
                if ch in ENEMIES and dist <= 2:
                    danger += 1
        return danger

    def is_my_bullet(self, pos):
        # prev result is fire and it's next cell in my direction
        return 'act' in self.result and pos == self.board.me.pos + self.board.me.dir.get_delta()

    def save_history(self, board):
        if self.SAVE_HISTORY:
            with open('history.txt', 'a') as file:
                n = int(math.sqrt(len(board)))
                for i in range(n):
                    file.write(board[i * n:(i + 1) * n] + '\n')
                file.write('\n')


