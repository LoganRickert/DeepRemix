import requests


class Game:
    def __init__(self, devkey, username, practice=True):
        if practice:
            url = 'http://aicomp.io/api/games/practice'
        else:
            url = 'http://aicomp.io/api/games/search'

        r = requests.post(url, data={'devkey': devkey, 'username': username})
        json = r.json()

        self.devkey = devkey
        self.url = url + json['gameID']
        self.playerID = json['playerID']

        return self, json

    def _submit_move(self, move):
        r = requests.post(self.url, data={'playerID': self.playerID,
            'move': move, 'devkey': self.devkey})
        return r.json()

    def drop_bomb(self):
        return self._submit_move('b')

    def do_nothing(self):
        return self._submit_move('')

    def move(self, direction):
        return self._submit_move('m' + direction[0])

    def turn(self, direction):
        return self._submit_move('t' + direction[0])

    def shoot_portal(self, color):
        return self._submit_move(color[0] + 'p')

    def buy(self, power_up):
        return self._submit_move('buy_' + power_up)
