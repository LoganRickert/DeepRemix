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

    def isCurrentLocationInDanger(self, state):
        return self.valueAtLocation(state, state.player_location) == 3

    def getSurvivableBombLocation(self, state, location):
        possibleLocations = self.reachableLocations(state, location)
        possibleSurvivableLocations = [bombLoc for bombLoc in possibleLocations if self.survivable(state, state.player_location, bombLoc)]
        
        bestSurvivable = sorted(locations, key=lambda x: self.numberOfTilesDestroyedByBombAtLocation(state, x))
        
        if len(bestSurvivable) == 0:
            return None

        return bestSurvivable[-1]
            
    def get_optimal_moves(self, state):
        if self.isCurrentLocationInDanger(state, state.player_location):
            return bestMoveOutOfDanger(state, state.player_location)

        bestSurvivableBombLocation = self.getSurvivableBombLocation(state, state.player_location)

        if bestSurvivableBombLocation is state.player_location:
            return ['b']
        else:
            return self.moveInDirectionOf(state, state.player_location, bestSurvivableBombLocation)

        return random.choice(['mr', 'md', 'ml', 'mu'])

    def valueAtLocation(self, state, tile):
        return state.board[tile.x][tile.y]

    # true if we are able to get out from bomb explosion in `tick` moves or less
    def survivable(self, state, currentLocation, bombLocation, tick=3):
        move = currentLocation
        
        length = 0
        
        while True:
            length = length + 1
            move = bestMoveOutOfDanger(state, move)
            if self.valueAtLocation(state, move) == 0:
                # it's safe t move here
                return (length <= tick)
            else:
                if length > tick:
                    return False

        return False


    def reachableLocations(self, state, loc):
        possibleTiles = []
    
    
    def moveInDirectionOf(self, state, start, finish):
    
    def bestMoveOutOfDanger(self, state, location):



