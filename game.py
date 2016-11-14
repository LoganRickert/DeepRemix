import requests


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameState:
    '''
    GameState is used to store the current state of the game

    '''
    def __init__(self, json):
        hard_tiles = json['hardBlockBoard']
        soft_tiles = json['softBlockBoard']
        blocked_tiles = [2 if h else 1 if s else 0 for h, s in
                zip(hard_tiles, soft_tiles)]
        self.board = [blocked_tiles[i: i + 11] for i in
                xrange(0, len(blocked_tiles), 11)]
        # transpose board
        self.board = map(list, zip(*self.board))

        self.completed = json['state'] == 'completed'

        self.player_location = Location(json['player']['x'],
                json['player']['y'])
        self.opponent_location = Location(json['opponent']['x'],
                json['opponent']['y'])

        self.board = self.bomb_effected_area(json['bombMap'])

    def bomb_effected_area(self, bomb_map):
        board = self.board
        range_ = 3
        locations = [Location(k[0], k[2]) for k, v in bomb_map.iteritems()]

        for loc in locations:
            for n in xrange(loc.x - range_, loc.x + range_):
                if n < 0 or n > 10:
                    continue
                if board[n][loc.y] != 2:
                    board[n][loc.y] = 3
            for n in xrange(loc.y - range_, loc.y + range_):
                if n < 0 or n > 10:
                    continue
                if board[loc.x][n] != 2:
                    board[loc.x][n] = 3

        return board

    def opponent_relative_location(self):
        return Location(self.player_location.x - self.opponent_location.x,
                self.player_location.y - self.opponent_location.y)


class Game:
    '''
    Game is used as a wrapper around the post requests with the server

    '''
    def __init__(self, devkey, username, practice=True, local=True):
        if local:
            url = 'http://localhost:80/'
        else:
            url = 'http://aicomp.io/'

        self.url = url + 'api/games/submit/'

        if practice:
            url += 'api/games/practice'
        else:
            url += 'api/games/search'

        response = requests.post(url, data={'devkey': devkey,
            'username': username}).json()

        print response

        self.url += response['gameID']
        self.playerID = response['playerID']
        self.devkey = devkey

        self.state = GameState(response)

    def _submit_move(self, move):
        print move
        data = {'playerID': self.playerID, 'move': move, 'devkey': self.devkey}
        print data
        response = requests.post(self.url, data)
        print response
        print self.url
        self.state = GameState(response.json())

    def submit_move(self, userMove):
        if userMove == 'b':
            self.drop_bomb()
        elif userMove == '':
            self.do_nothing()
        elif userMove[0] == 'm':
            self.move(userMove[-1:])
        elif userMove[0] == 't':
            self.turn(userMove[-1:])
        # need to add the other moves

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
