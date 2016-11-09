import random

from collections import defaultdict

from connectfour import Slot

def randargmax(a):
    return random.choice([i for i, x in enumerate(a) if x == max(a)])

class QLearningPlayer(object):
    def __init__(self, moves, epsilon = .2, alpha = .3, gamma = .9, initial = 1.):
        self.Q = defaultdict(lambda: initial)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def move(self, board):
        move = self.best_move(board)
        self.last_move = move
        print(move)
        return move

    def best_move(self, board):
        moves = board.available_moves()
        if random.random() < self.epsilon:
            return random.choice(moves)

        # print(self.Q)
        return randargmax([self.Q[x] for x in moves])

    def reward(self, board, value):
        raise NotImplementedError

class RandomPlayer(object):
    def __init__(self, moves):
        self.moves = moves

    def move(self, board):
        vals = [x for x in self.moves if board.col(x)[0] == Slot.empty]
        return random.choice(vals)

    def reward(self, board, value):
        pass
