from player import Player
from battle_city_client import BattleCityConnection


try:
    url = 'ws://dojorena.io/codenjoy-contest/ws?user=1nvdes0hwvkkoh3dfa21&code=1080829370632063683&gameName=battlecity'
    player = Player()
    ws = BattleCityConnection(url, player)
    ws.connect()
    ws.run_forever()
except KeyboardInterrupt:
    ws.close()
