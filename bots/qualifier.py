from bot import Bot
import random

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

    def get_optimal_moves(self, state):
#        if self.bombExplosionWillIntersectLocation(state,

        return []
