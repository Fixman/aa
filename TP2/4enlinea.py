from argparse import ArgumentParser
from collections import Counter

from connectfour import ConnectFour, WinnerState
from players import QLearningPlayer, RandomPlayer

players = {
    'random': RandomPlayer,
    'qlearn': QLearningPlayer,
}

def parse_args():
    parser = ArgumentParser(description = 'Juega al 4 en linea entre dos jugadores con Q-learning.')
    parser.add_argument('--games', type = int, default = 1000, help = 'Cantidad de juegos.')
    parser.add_argument('--players', type = str, nargs = 2, choices = players.keys(), default = ['qlearn', 'random'], help = 'Tipo de los jugadores.')
    args = parser.parse_args()

    args.player_types = [players[x] for x in args.players]
    return args

if __name__ == '__main__':
    args = parse_args()

    # Jugar entre un jugador que hace Q learning, y uno que juega al azar.
    a = args.player_types[0](ConnectFour.moves)
    b = args.player_types[1](ConnectFour.moves)

    # Acumular quien gana cada juego.
    c = Counter()
    for num in range(args.games):
        if num & (num - 1) == 0:
            print('Juego #{}'.format(num))

        game = ConnectFour(a, b)
        winner = game.play()
        c.update([winner.name])

        # Si este es el unico juego, imprimir el resultado.
        if args.games == 1:
            print(game.board.pretty_print())

    print(c)
    print('Red win ratio: {}'.format(c['red'] / args.games))
