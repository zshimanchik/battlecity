from visualizer_server.client import VisualizerClient
from constants import *

class Visualizer:
    def __init__(self):
        self.client = VisualizerClient('http://localhost:5000/')
        self.player = None

    def update(self, player):
        self.player = player
        # self.client.draw_text()
        self.client.draw_board(player.board.text)
        delta_vec = [0, 0]
        # for move in MOVES:
        #     if move in self.player.result:
        #         delta_vec = MOVE_TO_VEC[move]

        # if self.player.board.me is not None:
        #     self.client.buffer.append({'cmd': 'drawLine',
        #                                'row1': self.player.board.me.y,
        #                                'col1': self.player.board.me.x,
        #                                'row2': self.player.board.me.y + delta_vec[0],
        #                                'col2': self.player.board.me.x + delta_vec[1],
        #                                'color': [255,0,0] if 'ACT' in self.player.result else [0,0,0]})
        self.client.send_data()

    def print(self, text):
        self.client.print(text)

