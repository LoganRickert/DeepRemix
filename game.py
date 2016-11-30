import requests


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(" + repr(self.x) + ", " + repr(self.y) + ")"

    def up(self):
        return Location(self.x, self.y - 1)

    def down(self):
        return Location(self.x, self.y + 1)

    def right(self):
        return Location(self.x + 1, self.y)

    def left(self):
        return Location(self.x - 1, self.y)

    def __sub__(self, other):
        return Location(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y

    def __hash__(self):
        return hash(self.x**self.y)


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
#        self.board = map(list, zip(*self.board))

        self.completed = json['state'] == 'completed'

        self.player_location = Location(json['player']['x'],
                                        json['player']['y'])
        self.opponent_location = Location(json['opponent']['x'],
                                          json['opponent']['y'])
        self.player_index = json['playerIndex']
        self.alive = json['player']['alive']

        self.bomb_map = json['bombMap']
        self.board = self.bomb_effected_area(json['bombMap'])
        # board representation: board[x][y] = 3 if in bomb path, 2 if hard
        # block, 1 if soft block, 0 if nothing
        self.board[self.opponent_location.x][self.opponent_location.y] = -1

    def __repr__(self):
        out = ''
        for i in range(1, 10):
            for j in range(1, 10):
                if self.player_location.x == j and\
                        self.player_location.y == i:
                    out += "|^|"
                elif self.board[j][i] == 2:
                    out += "|*|"
                elif self.board[j][i] == 1:
                    out += "|#|"
                elif self.board[j][i] == 0:
                    out += "| |"
                elif self.board[j][i] == 3:
                    out += "|@|"
            out += '\n'

        return out

    def my_bomb_on_map(self):
        for k, v in self.bomb_map.iteritems():
            if v['owner'] == self.player_index:
                return True
        return False

    def loc_blocked(self, loc):
        return True if self.board[loc.x][loc.y] in (1, 2, -1) else False

    def legal_moves(self):
        '''
        returns the set of legal moves
        '''
        # TODO: add bomb, portal, buys
        legal_moves = set(['mu', 'md', 'mr', 'ml', ''])

        loc = self.player_location

        if self.loc_blocked(loc.up()):
            legal_moves.remove('mu')
        if self.loc_blocked(loc.down()):
            legal_moves.remove('md')
        if self.loc_blocked(loc.right()):
            legal_moves.remove('mr')
        if self.loc_blocked(loc.left()):
            legal_moves.remove('ml')

        return legal_moves

    def bomb_effected_area(self, bomb_map):
        board = self.board
        range_ = 3
        if isinstance(bomb_map, dict):
            locations = [Location(int(k[0]), int(k[2])) for k, v in
                         bomb_map.iteritems()]
        else:
            locations = [bomb_map]

        for loc in locations:
            for n in xrange(loc.x - range_, 1 + loc.x + range_):
                if n < 0 or n > 10:
                    continue
                if board[n][loc.y] not in (1, 2):
                    board[n][loc.y] = 3
            for n in xrange(loc.y - range_, 1 + loc.y + range_):
                if n < 0 or n > 10:
                    continue
                if board[loc.x][n] not in (1, 2):
                    board[loc.x][n] = 3

        return board

    def opponent_relative_location(self):
        return Location(self.player_location.x - self.opponent_location.x,
                        self.player_location.y - self.opponent_location.y)

    def __getitem__(self, loc):
        return set([location for location in [
            loc.up(), loc.down(), loc.right(), loc.left()]
            if not self.loc_blocked(location)])


class Game:
    '''
    Game is used as a wrapper around the post requests with the server

    '''
    def __init__(self, devkey, username, practice=True, game_id=None):
        url = 'http://aicomp.io/'
        self.url = url + 'api/games/submit/'

        if practice:
            url += 'api/games/practice'
        else:
            url += 'api/games/search'

        response = requests.post(
                url, data={'devkey': devkey, 'username': username}).json()

        if game_id:
            self.url += game_id
        else:
            self.url += response['gameID']

        self.playerID = response['playerID']
        self.devkey = devkey

        self.state = GameState(response)

    def submit_move(self, move):
        data = {'playerID': self.playerID, 'move': move, 'devkey': self.devkey}
        response = requests.post(self.url, data)
        self.state = GameState(response.json())
