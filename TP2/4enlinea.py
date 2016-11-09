from argparse import ArgumentParser

from connectfour import ConnectFour
from players import QLearningPlayer, RandomPlayer

def parse_args():
    parser = ArgumentParser(description = 'Juega al 4 en linea entre dos jugadores con Q-learning.')
    parser.add_argument('--games', type = int, default = 10000, help = 'Cantidad de juegos.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    a = RandomPlayer(ConnectFour.moves)
    b = RandomPlayer(ConnectFour.moves)

    game = ConnectFour(a, b)
    winner = game.play()
    print(game.board.pretty_print())
    print("Gano {}!".format(winner.name))
