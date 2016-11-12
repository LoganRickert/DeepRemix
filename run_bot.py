from game import Game

devkey = '582632dd3c0cc0ed06f9d05a'
username = 'mxms'


def findMove(game):
	board = game.board
	print game.playerLocation
	print game.opponentLocation

#	nearby = nearbyTiles(game.board, 

if __name__ == '__main__':
	game = Game(devkey, username, True)

	findMove(game)
