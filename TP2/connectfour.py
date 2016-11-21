from enum import Enum

# Un slot, que puede tener una ficha de un color o estar vacio.
class Slot(Enum):
    empty = 0
    red = 1
    blue = 2

# El estado de un tablero. Puede no estar ganando nadie, que este ganando
# algun jugador, o que haya un empate.
class WinnerState(Enum):
    null = 0
    red = 1
    blue = 2
    tie = 3

# Un tablero que empieza vacio, y se le puede agregar una ficha
# en alguna ranura.
class Board(object):
    rows = 6
    cols = 7

    # El estado inicial es con todos los slots vacios.
    def __init__(self):
        self.state = [[Slot.empty for x in range(self.cols)] for y in range(self.rows)]
        self.last_move = None

    # Dar una lista de movimienos validos, que tengan lugar para poner una ficha.
    def available_moves(self):
        return [x for x in range(self.cols) if self.col(x)[0] == Slot.empty]

    # Poner una ficha de algun color en alguna ranura.
    def put(self, color, move):
        last = max(x for x in range(self.rows) if self.state[x][move] == Slot.empty)
        self.state[last][move] = color
        # Guardo el último movimiento, utilizado por el minimax
        self.last_move = (last, move)
        return last, move

    def undo(self, x, y):
        self.state[x][y] = Slot.empty

    # Devolver una copia de una columna.
    def col(self, c):
        return [self.state[x][c] for x in range(self.rows)]

    def player_wins(self, color):
        if self.last_move:
            y, x = self.last_move
            return self.check_position(y,x) == WinnerState(color.value)
        return False

    def is_full(self):
        return False

    # Devolver si hay un cuatro-en-linea de algun jugador
    # empezando en el punto (y, x)
    def check_position(self, y, x):
        deltas = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1),
        ]

        if self.state[y][x] == Slot.empty:
            return None

        color = self.state[y][x]
        for dy, dx in deltas:
            p = 1
            for m in range(1, 4):
                try:
                    if self.state[y + dy * m][x + dx * m] != color:
                        break
                except IndexError:
                    break
                p += 1
            for m in range(-1, -4, -1):
                try:
                    if self.state[y + dy * m][x + dx * m] != color:
                        break
                except IndexError:
                    break
                p += 1

            if p >= 4:
                return WinnerState(color.value)

        return WinnerState.null

    # Devolver quien esta ganando.
    def winner(self, last):
        if last == None:
            return WinnerState.null

        return self.check_position(*last)

    # Imprimir el tablero de una manera linea y colorida.
    def pretty_print(self):
        colors = {
            # Slot.empty: '\033[1;37mo',
            Slot.empty: '\033[2;39mo\033[m',
            Slot.red: '\033[1;31mo\033[m',
            Slot.blue: '\033[1;34mo\033[m'
        }
        return '\n'.join(' '.join(colors[p] for p in q) for q in self.state)

# Un 4 en linea. Tiene un tablero y dos jugadores.
class ConnectFour(object):
    moves = range(7)

    # Inicializar el juego con los dos jugadores.
    def __init__(self, red, blue):
        self.board = Board()
        red.color = Slot.red
        red.enemy = Slot.blue
        blue.color = Slot.blue

        self.red = red
        self.blue = blue

    # Jugar al 4 en linea hasta que alguien gane o haya un empate.
    def play(self):
        current, opponent = self.red, self.blue
        last = None
        result = WinnerState.null
        for nmove in range(self.board.cols * self.board.rows):
            move = current.move(self.board)
            last = self.board.put(current.color, move)

            result = self.board.winner(last)
            if result != WinnerState.null:
                break
            current.reward(self.board, 0)
            current, opponent = opponent, current

        if result != WinnerState.null:
            winner, lower = opponent, current
            winner.reward(self.board, 1)
            lower.reward(self.board, -1)
        else:
            current.reward(self.board, .5)
            opponent.reward(self.board, .5)
            return WinnerState.tie

        return result
