import requests


class GameState:
    '''
    GameState is used to store the current state of the game

    '''
    def __init__(self, json):
        hard_tiles = json['hardBlockBoard']
        soft_tiles = json['softBlockBoard']
        blocked_tiles = []
        for h, s in zip(hard_tiles, soft_tiles):
            if h:
                blocked_tiles.append(2)
            elif s:
                blocked_tiles.append(1)
            else:
                blocked_tiles.append(0)


class Game:
    '''
    Game is used as a wrapper around the post requests with the server

    '''

    def __init__(self, devkey, username, practice=True, local=True):
        if local:
            url = 'http://localhost:80/'
        else:
            url = 'http://aicomp.io/'

        self.url = url + 'api/submit/'

        if practice:
            url += 'api/games/practice'
        else:
            url += 'api/games/search'

        response = requests.post(url, data={'devkey': devkey,
            'username': username}).json()

        self.url += response['gameID']
        self.playerID = response['playerID']
        self.devkey = devkey

        self.state = GameState(response)

    def _submit_move(self, move):
        response = requests.post(self.url, data={'playerID': self.playerID,
            'move': move, 'devkey': self.devkey}).json()
        self.state = GameState(response)

    def drop_bomb(self):
        self._submit_move('b')

    def do_nothing(self):
        self._submit_move('')

    def move(self, direction):
        self._submit_move('m' + direction[0])

    def turn(self, direction):
        self._submit_move('t' + direction[0])

    def shoot_portal(self, color):
        self._submit_move(color[0] + 'p')

    def buy(self, power_up):
        self._submit_move('buy_' + power_up)
