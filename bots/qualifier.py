from copy import deepcopy
from bot import Bot
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

    def directionBetweenMoves(self, loc, dest):
        if dest.y > loc.y:
            return 'mu'
        elif dest.y < loc.y:
            return 'md'
        elif dest.x < loc.x:
            return 'ml'
        elif dest.x > loc.x:
            return 'mr'
        return None

    def serialize(self, state, moves):
        ret = []

        lastMove = state.player_location

        for mov in moves:
            if isinstance(mov, Location):
                ret.append(self.directionBetweenMoves(lastMove, mov))
                lastMove = mov
            else:
                ret.append(mov)

        return ret

    def closestMoveOutOfDanger(self, state, loc):
        pass

    def lengthOfShortestPathOutOfDanger(self, state, loc):
        mov = loc
        length = 0

        while True:
            if self.tileIsWithinBombPath(state, mov):
                mov = self.closestMoveOutOfDanger(state, mov)
                length = length + 1
            else:
                break

        return length

    def tileIsWithinBombPath(self, state, loc):
        print "b" + repr(loc)
        return self.valueAtLocation(state, loc) == 3

    def bestSafeMoveTowardsEnemey(self, state, loc):
        pass

    def closestMoveOutOfDangerFromBomb(self, state, bomb_loc):
        st = deepcopy(state)
        st.board = self.bomb_effected_area(bomb_loc)
        return self.closestMoveOutOfDanger(st, bomb_loc)

    def possibleToSurviveDroppingBomb(self, state, loc, bomb_loc):
        # should just call closestMoveOutOfDangerFromBomb iteratively and
        # see if its less than 3
        mov = loc
        length = 0
        while True:
            # should be just > ?
            if length >= 3:
                return True
            if self.tileIsWithinBombPath(state, mov):
                mov = self.closestMoveOutOfDangerFromBomb(state, bomb_loc)
                length += 1
        return False

    def get_optimal_moves(self, state):
        print "a" + repr(state.player_location)
        if self.tileIsWithinBombPath(state, state.player_location):
            # in danger, move, hopefully towards opponent

            firstMove = self.closestMoveOutOfDanger(state,
                    state.player_location)
            secondMove = None

            if self.tileIsWithinBombPath(state, firstMove):
                secondMove = self.closestMoveOutOfDanger(state, firstMove)

            else:
                secondMove = self.bestSafeMoveTowardsEnemey(state, firstMove)

            return self.serialize(state, [firstMove, secondMove])
            # eh, just move towards enemy

        # not in range of bomb, see if there's a good place to put one

        movables = self.movableTiles(state, state.player_location)

        if len(movables) == 0:
            # nowhere to move, what do
            print "Nowhere to move. :("
            return

        possibleBombs = movables[:]
        possibleBombs.append(state.player_location)

        # have good moves, let's see if we can drop a bomb anywhere
        bestBombPlaces = self.mostBeneficialImmediateBombLocations(state,
                possibleBombs)

        # check to see if these kill you, are in-escapable

        bombLocation = None

        for pl in bestBombPlaces:
            if self.possibleToSurviveDroppingBomb(state, state.player_location,
                    pl):
                bombLocation = pl
                break

        if bombLocation is not None:
            if bombLocation.x == state.player_location.x and\
                    bombLocation.y == state.player_location.y:
                nextMove = self.closestMoveOutOfDangerFromBomb(state,
                        bombLocation)
                return self.serialize(state, ['b', nextMove])
            else:
                return self.serialize(state, [bombLocation, 'b'])

        else:
            pass
            # meh, just move somewhere in the right direction

        return self.serialize(state, [None, None])

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

    def mostBeneficialImmediateBombLocations(self, state, locations):

        return sorted(locations, key=lambda x:
                self.numberOfTilesDestroyedByBombAtLocation(state, x))

    def valueAtLocation(self, state, tile):
        print "c" + repr(tile)
        return state.board[tile.x][tile.y]

    def tileIsMovable(self, state, tile):
        return self.valueAtLocation(state, tile) == 0

    def movableTiles(self, state, loc):
        saneTiles = []

        lefTile = Location(loc.x - 1, loc.y)
        rightTile = Location(loc.x + 1, loc.y)
        topTile = Location(loc.x, loc.y - 1)
        bottomTile = Location(loc.x, loc.y + 1)

        if self.tileIsMovable(state, lefTile):
            saneTiles.append(lefTile)
        if self.tileIsMovable(state, rightTile):
            saneTiles.append(rightTile)
        if self.tileIsMovable(state, topTile):
            saneTiles.append(topTile)
        if self.tileIsMovable(state, bottomTile):
            saneTiles.append(bottomTile)

        return saneTiles
