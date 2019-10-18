
from flask import Flask, request, jsonify

class Receiver:

    def __init__(self, window):
        self.window = window
        self.flask_app = Flask(__name__)
        self.main_route = self.flask_app.route('/', methods=['POST'])(self.main_route)

    def main_route(self):
        print(request.data.decode('utf8'))
        self.window.data = request.get_json(silent=True)
        return "ok"

    def run(self):
        return self.flask_app.run()
