import random

from collections import defaultdict

from connectfour import Slot

# Elegir el argmax de una lista.
# Si hay varios valores iguales, elegir uno al azar.
def randargmax(a):
    return random.choice([i for i, x in enumerate(a) if x == max(a)])

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

    # Elegir el mejor movimiento, y anotarlo como ultimo movimiento.
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

        m = randargmax([self.Q[x] for x in moves])
        return moves[m]

    # Anotar el reward de una jugada.
    # Aca deberia estar la ecuacion Q.
    def reward(self, board, value):
        raise NotImplementedError

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
