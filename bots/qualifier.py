import random
from bot import Bot
from game import Location
import sys

boardSize = 11


class QualifierBot(Bot):
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
                if state.player_location.x == j and\
                        state.player_location.y == i:
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

    def isCurrentLocationInDanger(self, state, location):
        return self.valueAtLocation(state, location) == 3

    def getSurvivableBombLocation(self, state, location):
        possibleLocations = self.reachableLocations(state, location)
        possibleSurvivableLocations = [bombLoc for bombLoc in possibleLocations
                if self.survivable(state, state.player_location, bombLoc)]

        bestSurvivable = sorted(possibleSurvivableLocations, key=lambda x:
                self.numberOfTilesDestroyedByBombAtLocation(state, x))

        if len(bestSurvivable) == 0:
            return None

        return bestSurvivable[-1]

    def getRandomMove(self, state, loc):
        movableTiles = []

        lefTile = Location(loc.x - 1, loc.y)
        rightTile = Location(loc.x + 1, loc.y)
        topTile = Location(loc.x, loc.y - 1)
        bottomTile = Location(loc.x, loc.y + 1)

        if self.valueAtLocation(state, lefTile) == 0:
            movableTiles.append(lefTile)
        if self.valueAtLocation(state, rightTile) == 0:
            movableTiles.append(rightTile)
        if self.valueAtLocation(state, topTile) == 0:
            movableTiles.append(topTile)
        if self.valueAtLocation(state, bottomTile) == 0:
            movableTiles.append(bottomTile)

        return random.choice(movableTiles)

    def get_optimal_moves(self, state):
        if self.isCurrentLocationInDanger(state, state.player_location):
            print "In Danger!"
            return self.bestMoveOutOfDanger(state, state.player_location)

        print "Not in Danger."
        bestSurvivableBombLocation = self.getSurvivableBombLocation(state,
                state.player_location)

        print "Want to plant a bomb at " + repr(bestSurvivableBombLocation)
        if bestSurvivableBombLocation is state.player_location:
            print "Planting bomb"
            return 'b'
        else:
            print "Moving to plant a bomb"
            return self.moveInDirectionOf(state, state.player_location,
                    bestSurvivableBombLocation)

        return self.getRandomMove(state, state.player_location)

    def valueAtLocation(self, state, tile):
        return state.board[tile.x][tile.y]

    def survivable(self, state, currentLocation, bombLocation, tick=3):
        length = self.length_to_location(state, currentLocation,
                bombLocation)
        survivable = length <= tick

        print "Length from " + repr(currentLocation) + " to " +\
            repr(bombLocation) + ": " + repr(length)
        print "Survivable?: " + repr(survivable)

        return survivable

    def _reachableLocationSearch(self, state, loc, tiles):

        for t in tiles:
            if loc.x == t.x and loc.y == t.y:
                return False

        if self.valueAtLocation(state, loc) == 1 or\
                self.valueAtLocation(state, loc) == 2:
            return False
        else:
            tiles.append(loc)

        if ((loc.x < len(state.board) - 1 and self._reachableLocationSearch(
            state, Location(loc.x + 1, loc.y), tiles)) or
            (loc.y > 0 and self._reachableLocationSearch(state,
                Location(loc.x, loc.y - 1), tiles)) or
            (loc.x > 0 and self._reachableLocationSearch(state,
                Location(loc.x - 1, loc.y), tiles)) or
            (loc.y < len(state.board) - 1 and self._reachableLocationSearch(
                state, Location(loc.x, loc.y + 1), tiles))):
            return True

        return False

    def reachableLocations(self, state, loc):
        tiles = []
        self._reachableLocationSearch(state, loc, tiles)
        print "Reachable Locations: " + repr(tiles)
        return tiles

    def moveInDirectionOf(self, state, start, finish):
        print "Trying to move from " + repr(start) + " to " + repr(finish)
        legal_moves = state.legal_moves()
        print "Legal moves are: " + repr(legal_moves)
        relative_location = finish - start
        print "Relative location " + repr(relative_location)
        moves_to_relative_location = set()
        if relative_location.x > 0:
            moves_to_relative_location.add('mr')
        elif relative_location.x < 0:
            moves_to_relative_location.add('ml')
        if relative_location.y < 0:
            moves_to_relative_location.add('mu')
        elif relative_location.y > 0:
            moves_to_relative_location.add('md')
        print "Preferred moves are: " + repr(moves_to_relative_location)

        moves = moves_to_relative_location.intersection(legal_moves)
        print "Overlap is: " + repr(moves)

        if not moves:
            if not legal_moves:     # no legal moves, do nothing
                return ''
            return random.choice(tuple(legal_moves))
        else:
            return random.choice(tuple(moves))

    def bestMoveOutOfDanger(self, state, location):
        possibleLocations = self.reachableLocations(state, location)
        locations_out_of_danger = [bombLoc for bombLoc in possibleLocations if
                self.survivable(state, location, bombLoc)]
        print "Locations out of danger: " + repr(locations_out_of_danger)
        location_out_of_danger = sorted(locations_out_of_danger,
                key=lambda loc:
                self.length_to_location(state, location, loc))[0]
        print "Best location: " + repr(location_out_of_danger)

        return self.moveInDirectionOf(state, location, location_out_of_danger)

    def find_path(self, graph, start, finish, path=[]):
        path = path + [start]
        if start == finish:
            return path
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = self.find_path(graph, node, finish, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def length_to_location(self, state, start, finish):
        return len(self.find_path(state, start, finish))
