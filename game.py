import requests
import copy


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

        player_index = json['playerIndex']
        self.player = Player(json['player'], player_index)
        indices = [0, 1]
        indices.remove(player_index)
        opp_index = indices[0]
        self.opponent = Player(json['opponent'], opp_index)

        self.completed = json['state'] == 'completed'
        self.move_order = json['moveOrder']
        self.move_iterator = json['moveIterator']
        self.bomb_map = json['bombMap']
        self.portal_map = json['portalMap']

    def next_state(self, move):
        state = copy.deepcopy(self)

        # switch turn order
        index = state.move_order.index(state.move_iterator)
        if index == 0:
            state.move_iterator = state.move_order[1]
        else:
            state.move_order = state.move_order[::-1]

        return state

    def winner(self):
        assert self.completed
        assert not self.player.alive or not self.opponent.alive
        if self.player.alive:
            return self.player.id
        else:
            return self.opponent.id

    def legal_moves(self):
        '''
        returns the list of legal moves
        '''
        # TODO: add portals and turning, buy_block
        legal_moves = [
            'b', 'mu', 'md', 'mr', 'ml',
            'buy_range', 'buy_count', 'buy_pierce']

        loc = self.player.location

        if self._loc_blocked(loc.up()):
            legal_moves.remove('mu')
        if self._loc_blocked(loc.down()):
            legal_moves.remove('md')
        if self._loc_blocked(loc.right()):
            legal_moves.remove('mr')
        if self._loc_blocked(loc.left()):
            legal_moves.remove('ml')
        if self._bomb_at(loc):
            legal_moves.remove('b')
        if self.player.coins < 5:
            legal_moves.remove('buy_range')
            legal_moves.remove('buy_pierce')
            legal_moves.remove('buy_count')

        return legal_moves

    def _bomb_at(self, loc):
        return '%,%'.format(loc.x, loc.y) in self.bomb_map

    def _loc_blocked(self, loc):
        return True if self.board[loc.x][loc.y] in (1, 2, -1) else False

    def _bomb_effected_area(self, bomb_map):
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

    def __repr__(self):
        out = ''
        for i in range(1, 10):
            for j in range(1, 10):
                if self.player.location.x == j and\
                        self.player.location.y == i:
                    out += "|^|"
                elif self.board[j][i] == 2:
                    out += "|*|"
                elif self.board[j][i] == 1:
                    out += "|#|"
                elif self.board[j][i] == 0:
                    out += "| |"
                elif self.board[j][i] == 3:
                    out += "|@|"
                else:
                    out += "|x|"
            out += '\n'

        return out

    def __hash__(self):
        return hash(repr(self)) + hash(self.player) + hash(self.opponent)

    def __eq__(self, other):
        return hash(self) == hash(other)


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


class Player:
    def __init__(self, json, index):
        self.location = Location(json['x'], json['y'])
        self.orientation = json['orientation']
        self.id = index
        self.alive = json['alive']
        self.coins = json['coins']
        self.bomb_count = json['bombCount']
        self.bomb_range = json['bombRange']
        self.bomb_pierce = json['bombPierce']

    def __hash__(self):
        out = ''
        for k, v in self.__dict__.iteritems():
            if not k.startswith('__'):
                out += repr(v)
        return hash(out)
