import requests


class Game:
<<<<<<< HEAD
	
	def createBoard(self, hardTiles, softTiles):
		newArray = []
		for i in range(0, len(hardTiles)):
			if hardTiles[i] != 0:
				newArray.append(1)
			elif softTiles[i] != 0:
				newArray.append(2)
			else:
				newArray.append(0)
		return newArray


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
		self.playerInfo = json['player']
		self.opponentInfo = json['opponent']
		self.playerLocation = { 'x': self.playerInfo['x'], 'y': self.playerInfo['y'] }
		self.opponentLocation = { 'x': self.opponentInfo['x'], 'y': self.opponentInfo['y'] }
		self.board = self.createBoard(json['hardBlockBoard'], json['softBlockBoard'])
		print self.board

	def _submit_move(self, move):
		r = requests.post(self.url, data={'playerID': self.playerID, 'move': move, 'devkey': self.devkey})
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
=======
    def __init__(self, devkey, username, practice=True):
        if practice:
            url = 'http://aicomp.io/api/games/practice'
        else:
            url = 'http://aicomp.io/api/games/search'

        r = requests.post(url, data={'devkey': devkey, 'username': username})
        json = r.json()

        self.json = json
        self.devkey = devkey
        self.url = url + json['gameID']
        self.playerID = json['playerID']

    def get_json(self):
        return self.json

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
>>>>>>> 59f3edb8c90ba3390634bc694ecf825fdd193f20
