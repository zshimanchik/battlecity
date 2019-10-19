import threading

from flask import Flask, request
from werkzeug.serving import make_server


class Receiver(threading.Thread):

    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window
        self.flask_app = Flask(__name__)
        self.main_route = self.flask_app.route('/', methods=['POST'])(self.main_route)

        self.srv = make_server('127.0.0.1', 5000, self.flask_app)
        self.ctx = self.flask_app.app_context()
        self.ctx.push()

    def main_route(self):
        print(request.data.decode('utf8'))
        self.window.update(request.get_json(silent=True))
        return "ok"

    def run(self):
        print('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()
