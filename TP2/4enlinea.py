from argparse import ArgumentParser
from collections import Counter

from connectfour import ConnectFour, WinnerState
from players import QLearningPlayer, RandomPlayer

def parse_args():
    parser = ArgumentParser(description = 'Juega al 4 en linea entre dos jugadores con Q-learning.')
    parser.add_argument('--games', type = int, default = 10000, help = 'Cantidad de juegos.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    a = RandomPlayer(ConnectFour.moves)
    b = RandomPlayer(ConnectFour.moves)

    c = Counter()
    for _ in range(args.games):
        game = ConnectFour(a, b)
        winner = game.play()
        c.update([winner.name])

        if args.games == 1:
            print(game.board.pretty_print())

    print(c)
