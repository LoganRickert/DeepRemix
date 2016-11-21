import random
from bot import Bot
from game import Location
import sys
from copy import deepcopy

boardSize = 11


class QualifierBot(Bot):
    def __init__(self, state):
        self.states = [state]
        self.bombs_placed = set()

    def get_move(self, state):
        if not state.alive:
            print "YOU DIED."
            return
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

    def location_score(self, state, location, bomb_loc):
        n = 0
        range_ = 3
        for n in xrange(bomb_loc.x - range_, bomb_loc.x + range_):
            if n < 0 or n > 10:
                continue
            if state.board[n][bomb_loc.y] == 1:
                n += 1
        for n in xrange(bomb_loc.y - range_, bomb_loc.y + range_):
            if n < 0 or n > 10:
                continue
            if state.board[bomb_loc.x][n] == 1:
                n += 1

        tiles_destroyed = n
        length = self.length_to_location(state, location, bomb_loc)
        already_placed = 0.5 if bomb_loc in self.bombs_placed else 1

        return (already_placed * tiles_destroyed) - (.5 * length)

    def inDanger(self, state, location):
        return self.valueAtLocation(state, location) == 3

    def getSurvivableBombLocation(self, state, location):
        print "Figuring out where to plant a bomb."
        possibleLocations = self.reachableLocations(state, location)
        print "Possible locations: " + repr(possibleLocations)
        possibleSurvivableLocations = [bombLoc for bombLoc in possibleLocations
                if self.willSurviveBombPlacedAt(state, bombLoc)]
        print "Survivable locations: " + repr(possibleSurvivableLocations)

        if not possibleSurvivableLocations:
            return None

        return sorted(possibleSurvivableLocations, key=lambda bomb_loc:
                self.location_score(state, location, bomb_loc))[-1]

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
        if self.inDanger(state, state.player_location):
            print "In Danger!"
            return self.moveInDirectionOf(state, state.player_location,
                    self.bestLocationOutOfDanger(state, state.player_location))

        print "Not in Danger."
        if state.my_bomb_on_map() or self.states[-2].my_bomb_on_map():
            return None

        bestSurvivableBombLocation = self.getSurvivableBombLocation(state,
                state.player_location)

        print "Want to plant a bomb at " + repr(bestSurvivableBombLocation)
        if bestSurvivableBombLocation is state.player_location:
            print "Planting bomb"
            self.bombs_placed.add(state.player_location)
            return 'b'
        else:
            print "Moving to plant a bomb"
            return self.moveInDirectionOf(state, state.player_location,
                    bestSurvivableBombLocation)

        return self.getRandomMove(state, state.player_location)

    def valueAtLocation(self, state, tile):
        return state.board[tile.x][tile.y]

    def willSurviveBombPlacedAt(self, state, location, tick=4):
        st = deepcopy(state)
        st.bomb_effected_area(location)
        print "Testing bomb location: " + repr(location)
        safety = self.bestLocationOutOfDanger(st, location)
        print "Safe location found: " + repr(safety)
        if not safety:
            return False
        length_to_safety = self.length_to_location(st, location, safety)
        survivable = length_to_safety <= tick
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

    def bestLocationOutOfDanger(self, state, location):
        possibleLocations = self.reachableLocations(state, location)
        locations_out_of_danger = [loc for loc in possibleLocations if
                not self.inDanger(state, loc)]
        location_out_of_danger = sorted(locations_out_of_danger,
                key=lambda loc:
                self.length_to_location(state, location, loc))
        if location_out_of_danger:
            return location_out_of_danger[0]
        else:
            return None

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
        return shortest or range(20)

    def length_to_location(self, state, start, finish):
        return len(self.find_path(state, start, finish))
