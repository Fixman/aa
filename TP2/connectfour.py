from enum import Enum

class Point(Enum):
    empty = 0
    red = 1
    blue = 2

class WinnerState(Enum):
    null = 0
    red = 1
    blue = 2
    tie = 3

class Board(object):
    rows = 6
    cols = 7

    def __init__(self):
        self.state = [[Point.empty for x in range(self.cols)] for y in range(self.rows)]

    def put(self, color, move):
        self.state[max(x for x in range(self.rows) if self.state[x][move] == Point.empty)][move] = color

    def col(self, c):
        return [self.state[x][c] for x in range(self.rows)]
    
    def check_position(self, y, x):
        deltas = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        if self.state[y][x] == Point.empty:
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
                return WinnerState(color.value)

        return None

    def winner(self):
        available = False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.state[i][j] == Point.empty:
                    available = True
                else:
                    p = self.check_position(i, j)
                    if p:
                        return p

        if not available:
            return WinnerState.tie

        return WinnerState.null

    def pretty_print(self):
        colors = {
            # Point.empty: '\033[1;37mo',
            Point.empty: '\033[2;39mo\033[m',
            Point.red: '\033[1;31mo\033[m',
            Point.blue: '\033[1;34mo\033[m'
        }
        return '\n'.join(' '.join(colors[p] for p in q) for q in self.state)


class ConnectFour(object):
    moves = range(7)

    def __init__(self, red, blue):
        self.board = Board()
        red.color = Point.red
        blue.color = Point.blue

        self.red = red
        self.blue = blue

    def play(self):
        current, opponent = self.red, self.blue
        while self.board.winner() == WinnerState.null:
            move = current.move(self.board)
            self.board.put(current.color, move)

            current, opponent = opponent, current
        return self.board.winner()
