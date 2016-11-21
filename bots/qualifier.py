import random
from bot import Bot
import sys

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

        bestSurvivable = sorted(possibleSurvivableLocations, key=lambda x: self.numberOfTilesDestroyedByBombAtLocation(state, x))

        if len(bestSurvivable) == 0:
            return None

        return bestSurvivable[-1]

    def get_optimal_moves(self, state):
        if self.isCurrentLocationInDanger(state, state.player_location):
            return self.bestMoveOutOfDanger(state, state.player_location)

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
        return self.length_to_location(self, state, currentLocation, bombLocation) <= tick


    def reachableLocations(self, state, loc):
        possibleTiles = []


    def moveInDirectionOf(self, state, start, finish):
        legal_moves = state.legal_moves()
        relative_location = finish - start
        moves_to_relative_location = set()
        if relative_location.x > 0:
            moves_to_relative_location.add('mr')
        else:
            moves_to_relative_location.add('ml')
        if relative_location.y < 0:
            moves_to_relative_location.add('mu')
        else:
            moves_to_relative_location.add('md')

        moves = moves_to_relative_location.intersection(legal_moves)

        if not moves:   # no overlap between where you want to go and legal moves
            if not legal_moves:     # no legal moves, do nothing
                return ''
            return random.choice(tuple(legal_moves))    #choose a random legal move
        else:
            return random.choice(tuple(moves))  # move in the direction you want to go

    def bestMoveOutOfDanger(self, state, location):
        # called when bot is in danger
        possibleLocations = self.reachableLocations(state, location)
        locations_out_of_danger = [bombLoc for bombLoc in possibleLocations if self.survivable(state, state.player_location, bombLoc)]
        location_out_of_danger = sorted(locations_out_of_danger, key=lambda loc: self.length_to_location(state, loc))[0]

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
        graph = make_graph(state)
        return len(self.find_path(graph, start, finish))
