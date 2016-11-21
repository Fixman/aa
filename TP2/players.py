import copy
import random

from collections import defaultdict

from connectfour import Slot

# Elegir el argmax de una lista.
# Si hay varios valores iguales, elegir uno al azar.
def randargmax(a):
    mx = max(a)
    return random.choice([i for i, x in enumerate(a) if x == mx])

# Jugador que hace Q Learning.
class QLearningPlayer(object):
    # Inicializar jugador.
    # moves: lista de jugadas posibles.
    # epsilon: posibilidad de que el jugador haga un movimiento al azar.
    # alpha, gamma: valores de la ecuacion del Q-learning.
    # initial: valor inicial de los Q sin predicciones.
    def __init__(self, moves, epsilon = .2, alpha = .3, gamma = .9, initial = 1.):
        self.Q = defaultdict(lambda: initial)
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.last_move = None
        self.last_board = None

    # Elegir el mejor movimiento, y anotarlo como ultimo movimiento.
    # Tambien guardar estado anterior del tablero.
    def move(self, board):
        move = self.best_move(board)
        self.last_move = move
        return move

    # Elegir el mejor movimiento.
    # Con probabilidad epsilon, hacer un movimiento al azar.
    # Si no, elegir algun valor que tenga Q maximal.
    def best_move(self, board):
        moves = board.available_moves()
        if random.random() < self.epsilon:
            return random.choice(moves)

        m = randargmax([self.Q[board, x] for x in moves])
        return moves[m]

    # Anotar el reward de una jugada.
    # Aca deberia estar la ecuacion Q.
    def reward(self, board, value):
        if not self.last_move:
            return

        # Estoy bastante seguro de que esta ecuacion esta mal. Revisar.
        y = min(y for y in range(board.rows) if board.state[y][self.last_move] != Slot.empty)

        last_board = board
        previous = last_board.state[y][self.last_move]
        last_board.state[y][self.last_move] = Slot.empty

        maxq = max(self.Q[board, a] for a in board.available_moves())
        currq = self.Q[last_board, self.last_move]
        self.Q[last_board, self.last_move] = currq + self.alpha * ((value + self.gamma * maxq) - currq)

        last_board.state[y][self.last_move] = previous

# Jugador que hace jugadas al azar.
class RandomPlayer(object):
    def __init__(self, moves):
        self.moves = moves

    # Elegir un movimiento valido al azar.
    def move(self, board):
        return random.choice(board.available_moves())

    # No nos importa el reward.
    def reward(self, board, value):
        pass

class MinimaxPlayer(object):
    def __init__(self, moves):
        self.best_moves = {}
        # self.enemy = self.other(self.color)

    def other(self, value):
        if value == Slot.red:
            return Slot.blue
        else:
            return Slot.red

    def move(self, board):
        window = 5
        choices = []
        best_yet = -2
        for move in board.available_moves():
            row, column = board.put(self.color, move)
            self.minimax(1,1,1,1)
            board.undo(row, column)

        # if tuple(board) in self.best_moves:
        #     return random.choice(self.best_moves[tuple(board)])
        # if len(self.available_moves(board)) == 9:
        #     return random.choice([1,3,7,9])
        # best_yet = -2
        # choices = []
        # for move in self.available_moves(board):
        #     board[move-1] = self.me
        #     optimal = self.minimax(board, self.enemy, -2, 2)
        #     board[move-1] = ' '
        #     if optimal > best_yet:
        #         choices = [move]
        #         best_yet = optimal
        #     elif optimal == best_yet:
        #         choices.append(move)
        # self.best_moves[tuple(board)] = choices
        # return random.choice(choices)

        # self.minimax(1,1,1,1)
        return random.choice(board.available_moves())

    def minimax(self, board, char, alpha, beta):
        pass

    # No nos importa el reward.
    def reward(self, board, value):
        pass
