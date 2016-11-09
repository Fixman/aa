import random

from collections import defaultdict

from connectfour import Point

class QLearningPlayer(object):
    def __init__(self, moves, epsilon = .2, alpha = .3, gamma = .9):
        self.q = defaultdict(lambda: random.choice(moves))
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def move(self, board):
        raise NotImplementedError

    def reward(self, value, board):
        raise NotImplementedError

    def Q(self, board, action):
        raise NotImplementedError

class RandomPlayer(object):
    def __init__(self, moves):
        self.moves = moves

    def move(self, board):
        vals = [x for x in self.moves if board.col(x)[0] == Point.empty]
        return random.choice(vals)

    def reward(self, value, board):
        pass

