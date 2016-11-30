from abc import ABCMeta, abstractmethod


class Bot:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, state):
        pass

    @abstractmethod
    def get_move(self, state, legal_moves=None):
        pass
