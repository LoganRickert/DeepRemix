from bot import Bot
import random
from game import Location

boardSize = 11

def sgn(x):
    if x < 0:
        return -1
    else:
        return 1
    return 0

class QualifierBot(Bot):
    bombs = []

    def __init__(self, state):
        self.states = [state]

    def get_move(self, state):
        self.states.append(state)

        return self.get_optimal_moves(state)

    def closestMoveOutOfDanger(self, state, loc):



    def get_optimal_moves(self, state):
        movables = self.movableTiles(state, state.player_location)

        print "Can move to " + repr(movables)

        if len(movables) == 0:
            # we're in a space where a bomb is. let's find the closest place out

            return


        # have good moves, let's see if we can drop a bomb anywhere
        bestBombPlaces = self.mostBeneficialImmediateBombLocations(state, state.player_location)
        # check to see if these kill you, are in-escapable


        return []

    def mostBeneficialImmediateBombLocations(self, state, loc):
        possibleBombLocations = self.movableTiles(state, loc)

        return sorted(possibleBombLocations, key=lambda x
                numberOfTilesDestroyedByBombAtLocation(state, x))

    def numberOfTilesDestroyedByBombAtLocation(self, state, loc):
        n = 0
        range_ = 3
        for n in xrange(loc.x - range_, loc.x + range_):
            if n < 0 or n > 10:
                continue
            if state.board[n][loc.y] == 1:
                n += 1
        for n in xrange(loc.y - range_, loc.y + range_):
            if n < 0 or n > 10:
                continue
            if state.board[loc.x][n] == 1:
                n += 1

        return n

    def valueAtLocation(self, state, tile):
        return state.board[tile.x][tile.y]

    def tileIsMovable(self, state, tile):
        return self.valueAtLocation(state, tile) == 0

    def movableTiles(self, state, loc):
        saneTiles = []

        lefTile = Location(loc.x - 1, loc.y)
        rightTile = Location(loc.x + 1, loc.y)
        topTile = Location(loc.x, loc.y - 1)
        bottomTile = Location(loc.x, loc.y + 1)
        currentTile = loc

        if self.tileIsMovable(state, lefTile):
            saneTiles.append(lefTile)
        if self.tileIsMovable(state, rightTile):
            saneTiles.append(rightTile)
        if self.tileIsMovable(state, topTile):
            saneTiles.append(topTile)
        if self.tileIsMovable(state, bottomTile):
            saneTiles.append(bottomTile)

        return saneTiles
