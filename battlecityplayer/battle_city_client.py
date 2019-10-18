from ws4py.client.threadedclient import WebSocketClient
import time


class BattleCityConnection(WebSocketClient):
    def __init__(self, url, player):
        super(BattleCityConnection, self).__init__(url)
        self.player = player
        self.prev_time = time.time()

    def received_message(self, message):
        board = str(message).lstrip("board=")
        time_waited = time.time() - self.prev_time
        self.prev_time = time.time()
        response = self.player.turn(board)
        time_thinking = time.time() - self.prev_time
        self.prev_time = time.time()
        self.send(response)
        time_sending = time.time() - self.prev_time
        self.prev_time = time.time()
        print(f'W: {time_waited:.3f} T: {time_thinking:.3f} S: {time_sending:.3f}')

