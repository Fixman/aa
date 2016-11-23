import pandas
import matplotlib
import seaborn
import itertools
import numpy

from matplotlib import pyplot
from collections import Counter
from collections import defaultdict

from players import RandomPlayer, QLearningPlayer
from connectfour import ConnectFour, WinnerState

pyplot.rcParams['figure.figsize'] = 12, 6

def playAndPlot(red, blue, games = 1000):
    plotGames(playGames(red, blue, games), [type(red).__name__, type(blue).__name__])

def playGames(red, blue, games = 1000):
    return numpy.array([ConnectFour(red, blue).play() for _ in range(games)])

def plotGames(games, players):
    x = numpy.arange(games.size)
    states = [WinnerState.red, WinnerState.blue]
    for state, player in zip(states, players):
        y = numpy.cumsum(games == state) / (x + 1)
        pyplot.plot(x, y, label = player, color = state.name)

    pyplot.legend()
    pyplot.xlabel('Juegos')
    pyplot.ylabel('Proporcion juegos ganados')

def test_gamma():
    random = RandomPlayer(ConnectFour.moves)
    games = 10000
    colors = ['b', 'g', 'r', 'c', 'm']
    i = 0
    for g in numpy.arange(0.1, 1, 0.2):
        qlearn = QLearningPlayer(ConnectFour.moves, gamma=g)
        results = playGames(qlearn, random, games)
        x = numpy.arange(games)
        y = numpy.cumsum(results == WinnerState.red) / (x + 1)
        pyplot.plot(x, y, label = 'gamma = {}'.format(g), color = colors[i])
        i += 1

    pyplot.legend()
    pyplot.xlabel('Juegos')
    pyplot.ylabel('Proporción juegos ganados')
    pyplot.savefig('gamma.png')

def test_epsilon():
    random = RandomPlayer(ConnectFour.moves)
    games = 10000
    colors = ['b', 'g', 'r', 'c', 'm']
    i = 0
    for e in numpy.arange(0.1, 1, 0.2):
        qlearn = QLearningPlayer(ConnectFour.moves, epsilon=e)
        results = playGames(qlearn, random, games)
        x = numpy.arange(games)
        y = numpy.cumsum(results == WinnerState.red) / (x + 1)
        pyplot.plot(x, y, label = 'epsilon = {}'.format(e), color = colors[i])
        i += 1

    pyplot.legend()
    pyplot.xlabel('Juegos')
    pyplot.ylabel('Proporción juegos ganados')
    pyplot.savefig('epsilon.png')

# test_gamma()
test_epsilon()
