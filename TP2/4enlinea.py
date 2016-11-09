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

class RandomPlayer(object):
    def __init__(self, moves):
        self.moves = moves

    def move(self, board):
        vals = [x for x in range(self.moves) if board.col(x)[0] == board.Point.empty]
        return random.choice(vals)

    def reward(self, value, board):
        pass

class ConnectFour(object):
    moves = 7

    class Board(object):
        rows = 6
        cols = 7

        class Point(Enum):
            empty = 0
            red = 1
            blue = 2

        class WinnerState(Enum):
            null = 0
            red = 1
            blue = 2
            tie = 3

        def __init__(self):
            self.state = [[self.Point.empty for x in range(self.cols)] for y in range(self.rows)]

        def put(self, color, move):
            self.state[max(x for x in range(self.rows) if self.state[x][move] == self.Point.empty)][move] = color

        def col(self, c):
            return [self.state[x][c] for x in range(self.rows)]
        
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
                for m in range(4):
                    try:
                        if self.state[y + dy * m][x + dx * m] != color:
                            break
                    except IndexError:
                        break
                else:
                    return color

            return None

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

        def pretty_print(self):
            colors = {
                # self.Point.empty: '\033[1;37mo',
                self.Point.empty: '\033[1;37mo\033[m',
                self.Point.red: '\033[0;31mo\033[m',
                self.Point.blue: '\033[0;34mo\033[m'
            }
            return '\n'.join(' '.join(colors[p] for p in q) for q in self.state)


    def __init__(self, red, blue):
        self.board = self.Board()
        red.color = self.Board.Point.red
        blue.color = self.Board.Point.blue

        self.red = red
        self.blue = blue

    def play(self):
        current, opponent = self.red, self.blue
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
    # print(" "+ "\033[01;41m" + " " +"\033[01;46m"  + "  " + "\033[01;42m")
    args = parse_args()

    a = RandomPlayer(ConnectFour.moves)
    b = RandomPlayer(ConnectFour.moves)

    game = ConnectFour(a, b)
    winner = game.play()
    print(game.board.pretty_print())
    print("Gano {}!".format(winner.name))
