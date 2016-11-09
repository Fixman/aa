import random

from argparse import ArgumentParser
from collections import defaultdict
from enum import Enum

class QLearningPlayer(object):
    def __init__(self, moves, epsilon = .2, alpha = .3, gamma = .9):
        self.q = defaultdict(lambda: random.randrange(moves))
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def move(self, board):
        raise NotImplementedError

    def reward(self, value, board):
        raise NotImplementedError

    def Q(self, board, action):
        raise NotImplementedError

class ConnectFour(object):
    rows = 6
    cols = 7
    moves = cols

    class Point(Enum):
        empty = 0
        red = 1
        white = 2

    def __init__(self, red, white, rows = 6, cols = 7):
        self.board = [[self.Point.empty for x in range(cols)] for y in range(rows)]

    def play(self):
        raise NotImplementedError

def parse_args():
    parser = ArgumentParser(description = 'Juega al 4 en linea entre dos jugadores con Q-learning.')
    parser.add_argument('--games', type = int, default = 10000, help = 'Cantidad de juegos.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    a = QLearningPlayer(ConnectFour.moves)
    b = QLearningPlayer(ConnectFour.moves)

    for _ in range(args.games):
        ConnectFour(a, b).play()
