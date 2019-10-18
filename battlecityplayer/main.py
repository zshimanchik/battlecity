from player import Player
from battle_city_client import BattleCityConnection

try:
    from visualizer import Visualizer
    visualizer = Visualizer()
except Exception:
    from unittest.mock import Mock
    visualizer = Mock()

try:
    url = 'ws://dojorena.io/codenjoy-contest/ws?user=1nvdes0hwvkkoh3dfa21&code=1080829370632063683&gameName=battlecity'
    player = Player(visualizer)
    ws = BattleCityConnection(url, player)
    ws.connect()
    ws.run_forever()
except KeyboardInterrupt:
    ws.close()
