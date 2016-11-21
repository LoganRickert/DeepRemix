import random
from copy import deepcopy
from bot import Bot
import sys
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
        print "=================================="
        print "STARTING NEW STATE: "
        self.printBoard(state)

        return self.get_optimal_moves(state)

    def printBoard(self, state):
        for i in range(1, 10):
            for j in range(1, 10):
                if state.player_location.x == j and state.player_location.y == i:
                    sys.stdout.write("|^|")
                elif state.board[j][i] == 2:
                    sys.stdout.write("|*|")
                elif state.board[j][i] == 1:
                    sys.stdout.write("|#|")
                elif state.board[j][i] == 0:
                    sys.stdout.write("| |")
                elif state.board[j][i] == 3:
                    sys.stdout.write("|@|")
            print ""

    def directionBetweenMoves(self, loc, dest):
        if dest.y < loc.y:
            return 'mu'
        elif dest.y > loc.y:
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

    def recursiveSearchForSafety(self, state, loc, prev):
        initialStates = self.immediateMovableTilesNearby(state, loc)

        for st in initialStates:
            if prev is not None and (st.x != prev.x or st.y != prev.y):
                if self.valueAtLocation(state, st) == 0:
                    return 1
                elif self.valueAtLocation(state, st) == 3:
                    return 1 + self.recursiveSearchForSafety(state, st, loc)
        return 100000

    def immediateMovableTilesNearby(self, state, loc):
        ret = []

        leftTile = Location(loc.x - 1, loc.y)
        rightTile = Location(loc.x + 1, loc.y)
        topTile = Location(loc.x, loc.y - 1)
        bottomTile = Location(loc.x, loc.y + 1)
        if self.valueAtLocation(state, leftTile) not in (1, 2):
            ret.append(leftTile)
        if self.valueAtLocation(state, rightTile) not in (1, 2):
            ret.append(rightTile)
        if self.valueAtLocation(state, topTile) not in (1, 2):
            ret.append(topTile)
        if self.valueAtLocation(state, bottomTile) not in (1, 2):
            ret.append(bottomTile)
        
        return ret

    def closestMoveOutOfDanger(self, state, loc):
        # divide and conquer

        initialStates = self.immediateMovableTilesNearby(state, loc)
        
        print "[closestMoveOutOfDanger] Initial states: " + repr(initialStates)

        if len(initialStates) == 0:
            print "nowhere to move out of danger"
            return loc  # nowhere to move

        minimumState = None
        minimumStateLength = 100000     # a sufficiently big number

        for st in initialStates:
            length = self.recursiveSearchForSafety(state, st, None)
            if length <= minimumStateLength:
                minimumState = st
                minimumStateLength = length

        print "[closestMoveOutOfDanger] Best move out of danger: " + repr(minimumState)

        if minimumState is None:
            # wat? i guess return anything...
            pass
        else:
            return minimumState

    def lengthOfShortestPathOutOfDanger(self, state, loc):
        mov = loc
        length = 0

        while True:
            if self.tileIsWithinBombPath(state, mov):
                mov = self.closestMoveOutOfDanger(state, mov)
                print "[lengthOfShortestPathOutOfDanger] Moving along path  " + repr(mov)
                length = length + 1
                if length >= 5:
                    return length
            else:
                break

        return length

    def tileIsWithinBombPath(self, state, loc):
        return self.valueAtLocation(state, loc) == 3

    def bestSafeMoveTowardsEnemey(self, state, loc):
        # assumptions: not already in bomb path
        legal_moves = state.legal_moves()
        rel_loc = state.opponent_relative_location()

        opp_move = set()
        if rel_loc.x > 0:
            opp_move.add('mr')
        else:
            opp_move.add('ml')
        if rel_loc.y < 0:
            opp_move.add('mu')
        else:
            opp_move.add('md')

        moves = opp_move.intersection(legal_moves)

        if not moves:
            if not legal_moves:
                return ''
            return random.choice(tuple(legal_moves))
        else:
            return random.choice(tuple(moves))

    def closestMoveOutOfDangerFromBomb(self, state, bomb_loc):
        st = deepcopy(state)
        st.board = state.bomb_effected_area(bomb_loc)
        return self.closestMoveOutOfDanger(st, bomb_loc)

    def possibleToSurviveDroppingBomb(self, state, loc, bomb_loc):
        # should just call closestMoveOutOfDangerFromBomb iteratively and
        # see if its less than 3
        
        st = deepcopy(state)
        st.board = state.bomb_effected_area(bomb_loc)
        
        length = self.lengthOfShortestPathOutOfDanger(st, loc)

        return length <= 3
    

    def get_optimal_moves(self, state):
        if self.tileIsWithinBombPath(state, state.player_location):
            # in danger, move, hopefully towards opponent

            firstMove = self.closestMoveOutOfDanger(state, state.player_location)
            
            return self.serialize(state, [firstMove])
            # eh, just move towards enemy

        # not in range of bomb, see if there's a good place to put one

        movables = self.movableTiles(state, state.player_location)

        if len(movables) == 0:
            # nowhere to move, what do
            print "Nowhere to move. :("
            return self.serialize(state, [None, None])

        possibleBombs = movables[:]
        possibleBombs.append(state.player_location)

        # have good moves, let's see if we can drop a bomb anywhere
        bestBombPlaces = self.mostBeneficialImmediateBombLocations(state, possibleBombs)

        # check to see if these kill you, are in-escapable

        bombLocation = None

        for pl in bestBombPlaces:
            
            if self.possibleToSurviveDroppingBomb(state, state.player_location, pl):
                print "??? can survive"
                bombLocation = pl
                break
        
        print repr(state.player_location)

        if bombLocation:
            print "found a good bomb loc" + repr(bombLocation.x) + " " + repr(bombLocation.y)
            if bombLocation.x == state.player_location.x and bombLocation.y == state.player_location.y:
                nextMove = self.closestMoveOutOfDangerFromBomb(state, bombLocation)
                print "i am here"
                return self.serialize(state, ['b'])
            else:
                print "fuck me"
                return self.serialize(state, [bombLocation])

        else:
#            return [self.bestSafeMoveTowardsEnemey(state, state.player_location)]
            pass
            # meh, just move somewhere in the right direction

        return self.serialize(state, [None])

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
