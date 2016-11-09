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

    # Dar una lista de movimienos validos, que tengan lugar para poner una ficha.
    def available_moves(self):
        return [x for x in range(self.cols) if self.col(x)[0] == Slot.empty]

    # Poner una ficha de algun color en alguna ranura.
    def put(self, color, move):
        try:
            self.state[max(x for x in range(self.rows) if self.state[x][move] == Slot.empty)][move] = color
        except ValueError:
            import ipdb
            ipdb.set_trace()

    # Devolver una copia de una columna.
    def col(self, c):
        return [self.state[x][c] for x in range(self.rows)]
    
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
            for m in range(4):
                try:
                    if self.state[y + dy * m][x + dx * m] != color:
                        break
                except IndexError:
                    break
            else:
                return WinnerState(color.value)

        return None

    # Devolver quien esta ganando.
    def winner(self):
        available = False
        for i in range(self.rows):
            for j in range(self.cols):
                if self.state[i][j] == Slot.empty:
                    available = True
                else:
                    p = self.check_position(i, j)
                    if p:
                        return p

        if not available:
            return WinnerState.tie

        return WinnerState.null

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
        blue.color = Slot.blue

        self.red = red
        self.blue = blue

    # Jugar al 4 en linea hasta que alguien gane o haya un empate.
    def play(self):
        current, opponent = self.red, self.blue
        while self.board.winner() == WinnerState.null:
            move = current.move(self.board)
            self.board.put(current.color, move)

            current, opponent = opponent, current
        return self.board.winner()
