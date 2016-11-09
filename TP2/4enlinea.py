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
    moves = 7

    class Board(object):
        rows = 6
        cols = 7

        class Point(Enum):
            empty = 0
            red = 1
            white = 2

        class WinnerState(Enum):
            null = 0
            red = 1
            white = 2
            tie = 3

        def __init__(self):
            self.state = [[self.Point.empty for x in range(self.cols)] for y in range(self.rows)]

        def put(self, color, move):
            self.board[max(x for x in board if board[x] == Point.empty)] = color
        
        def check_position(self, y, x):
            deltas = [
                (0, 1),
                (1, 0),
                (1, 1),
                (1, -1),
            ]

            if self.state[y][x] == self.Point.empty:
                return None

            color = self.state[y][x]
            for dy, dx in deltas:
                for m in range(3):
                    try:
                        if self.state[y + dy * m][x + dx * m] != color:
                            return None
                    except IndexError:
                        break

            return color

        def winner(self):
            available = False
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.state[i][j] == self.Point.empty:
                        available = True
                    else:
                        p = self.check_position(i, j)
                        if p:
                            return p

            if not available:
                return self.WinnerState.tie

            return self.WinnerState.null

    def __init__(self, red, white):
        self.board = self.Board()
        red.color = self.Board.Point.red
        white.color = self.Board.Point.white

        self.red = red
        self.white = white

    def play(self):
        current, opponent = self.red, self.white
        print(self.board.winner())
        while self.board.winner() == self.Board.WinnerState.null:
            move = current.move(self.board)
            self.board.put(current.color, move)

            current, opponent = opponent, current
        return self.board.winner()

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
