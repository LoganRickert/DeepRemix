from game import Game

devkey = '582632dd3c0cc0ed06f9d05a'
username = 'mxms'

def isTileInBoard(board, tile):
	return tile['x'] < 10 and tile['x'] > 0 and tile['y'] > 0 and tile['y'] < 1

def tileValueAtLocation(board, loc):
	return board[loc['x']*9 + loc['y']]

def isTileMoveable(board, loc):
	return isTileInBoard(board, loc) and tileValueAtLocation(board, loc) == 0

def nearbyTiles(board, loc):
	validTiles = []
	leftTile = { 'x': loc['x'] - 1, 'y': loc['y'] }
	rightTile = { 'x': loc['x'], 'y': loc['y'] + 1 }
	topTile = { 'x': loc['x'], 'y': loc['y'] + 1 }
	bottomTile = { 'x': loc['x'], 'y': loc['y'] - 1 }
	
	if isTileMoveable(board, leftTile):
		validTiles.append(leftTile)
	
	if isTileMoveable(board, rightTile):
		validTiles.append(rightTile)

	if isTileMoveable(board, topTile):
		validTiles.append(topTile)

	if isTileMoveable(board, bottomTile):
		validTiles.append(bottomTile)

	return validTiles

def destroyedTilesFromBombAtLocation(game, tile):
	# meh
	return []


def findMove(game):
	board = game.board
	print game.playerLocation
	print game.opponentLocation

	nearby = nearbyTiles(game.board, game.playerLocation)

	maxDestroyedCount = 0
	maxDestroyPosition = {}

	for t in nearby:
		destroyCount = destroyedTilesFromBombAtLocation(game, t)
		if (destroyCount > maxDestroyedCount):
			maxDestroyedCount = destroyCount
			maxDestroyPosition = t

	print maxDestroyPosition
	print maxDestroyedCount

if __name__ == '__main__':
	game = Game(devkey, username, True)

	findMove(game)
