from bot import Bot


class QualifierBot(Bot):
    def __init__(self, state):
        self.states = [state]

    def get_move(self, state):
        self.states.append(state)
