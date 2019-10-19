import requests


class VisualizerClient:
    def __init__(self, server):
        self.server = server
        self.buffer = []

    def send_data(self):
        try:
            resp = requests.post(self.server, json=self.buffer, timeout=0.2)
            print(resp)
        except Exception as ex:
            print('Canot send data, cause ', ex)
        self.buffer.clear()

    def set_pen(self, r, g ,b):
        self.buffer.append({
            'cmd': 'setPen',
            'color': [r,g,b],
        })

    def draw_text(self, x, y, text):
        self.buffer.append({
            'cmd': 'drawText',
            'x': x,
            'y': y,
            'text': text
        })

    def draw_board(self, board):
        self.buffer.append({
            'cmd': 'drawBoard',
            'board': board
        })

    def print(self, text):
        print(text)
        self.buffer.append({
            'cmd': 'print',
            'text': text,
        })

    def draw_line(self, x1, y1, x2, y2, color=None):
        self.buffer.append({
            'cmd': 'drawLine',
            'x1': x1, 'y1': y1,
            'x2': x2, 'y2': y2,
            'color': [0,0,0] if color is None else color,
        })

    def draw_rect(self, x, y):
        self.buffer.append({
            'cmd': 'drawRect',
            'x': x,
            'y': y,
        })




