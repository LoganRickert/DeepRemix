from abc import ABCMeta, abstractmethod


class Bot:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_move(self, state):
        pass
