import logging
from collections import deque

from models import Board
from tactics.hunt import Hunt
from tactics.random import RandomTactics
from tactics.see_and_shoot import SeeAndShoot

logger = logging.getLogger(__name__)


class Player:
    tactics = [
        RandomTactics(),
        SeeAndShoot(),
        Hunt(),
    ]

    FIRE_COUNTDOWN = 4

    def __init__(self, visualizer):
        self.board = None
        self.visualizer = visualizer
        self.history = deque(maxlen=3)
        self.fire_countdown = 0

    def turn(self, board):
        try:
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
            print("Dead. Do nothing")
            return ''

        print(f'fc={self.fire_countdown}')
        for tactic in self.tactics:
            tactic.update(self)

        print('\n'.join('{t.usability:.3f} {t.action} {t.__class__.__name__}'.format(t=t) for t in self.tactics))

        current_tactics = max(self.tactics, key=lambda t: t.usability)
        action = current_tactics.action
        if 'act' in action:
            self.fire_countdown = self.FIRE_COUNTDOWN
        assert isinstance(action, str)
        # return 'right,act'
        return action

    def tick(self):
        if self.fire_countdown > 0:
            self.fire_countdown -= 1

