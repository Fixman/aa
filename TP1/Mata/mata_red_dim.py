from __future__ import print_function
from __future__ import division

import numpy
import scipy
import pandas
import matplotlib
import seaborn

from sklearn.feature_selection import SelectKBest, SelectPercentile, chi2
from sklearn.naive_bayes import BernoulliNB
from sklearn.cross_validation import cross_val_score
from sklearn.neighbors import KNeighborsClassifier

from matplotlib import pyplot

def select_k_best(k, features, spam):
    return SelectKBest(chi2, k=k).fit_transform(features, spam)

def select_percentile(p, features, spam):
    return SelectPercentile(chi2, percentile=p).fit_transform(features, spam)

def main():
    # features_csv = "../dev/body_word_features.csv"
    features_csv = "../dev/subject_word_features.csv"

    folds = 3
    nb = BernoulliNB(alpha = 1, fit_prior = True)
    # kn = KNeighborsClassifier(2, weights = 'uniform')

    features = pandas.read_csv(features_csv, index_col='num')
    spam = pandas.read_csv("../data/train.csv", usecols=['spam'])
    spam = spam.ix[:, 0]

    k_best_arange = numpy.arange(10,201,10)
    percentil_arange = numpy.arange(10, 101, 10)
    bernoulli = []

    for k in percentil_arange:
        # reduced_features = select_k_best(k, features, spam)
        reduced_features = select_percentile(k, features, spam)
        bernoulli.append(sum(cross_val_score(nb, reduced_features, spam, cv = folds)) / folds)
        # k_neighbors.append(sum(cross_val_score(kn, reduced_features, spam, cv = folds)) / folds)
        print("processing")

    print(bernoulli)

def plot():
    k_best_arange = numpy.arange(10,201,10)
    percentil_arange = map(lambda x: x*2, numpy.arange(10, 101, 10))
    bernoulli_body_k_best = [0.77424691358024689, 0.79553086419753083, 0.81732098765432104, 0.83055555555555538, 0.83392592592592596, 0.84292592592592597, 0.84845679012345687, 0.85119753086419758, 0.85383950617283955, 0.85849382716049372, 0.86330864197530877, 0.86612345679012348, 0.86786419753086419, 0.86918518518518517, 0.87225925925925918, 0.87251851851851858, 0.87269135802469133, 0.87429629629629624, 0.87427160493827161, 0.87395061728395051]
    bernoulli_body_percentile = [0.79553086419753083, 0.83055555555555538, 0.84292592592592597, 0.85119753086419758, 0.85849382716049372, 0.86612345679012348, 0.86918518518518517, 0.87251851851851858, 0.87429629629629624, 0.87395061728395051]
    bernoulli_subject_k_best = [0.53428395061728395, 0.54733333333333334, 0.57234567901234568, 0.56291358024691363, 0.56875308641975308, 0.5850864197530864, 0.58939506172839506, 0.59199999999999997, 0.59943209876543213, 0.60277777777777775, 0.60488888888888892, 0.60722222222222222, 0.61013580246913579, 0.61203703703703705, 0.61311111111111105, 0.61592592592592588, 0.61708641975308642, 0.61649382716049383, 0.61611111111111105, 0.61550617283950615]
    bernoulli_subject_percentile = [0.54733333333333334, 0.56291358024691363, 0.5850864197530864, 0.59199999999999997, 0.60277777777777775, 0.60722222222222222, 0.61203703703703705, 0.61592592592592588, 0.61649382716049383, 0.61550617283950615]

    pyplot.plot(k_best_arange, bernoulli_body_k_best, color="blue", linewidth = 2.0, linestyle="-", label= "Body features, K-Best selection")
    pyplot.plot(percentil_arange, bernoulli_body_percentile, color="blue", linewidth = 2.0, linestyle="--", label= "Body features, Percentile selection")
    pyplot.plot(k_best_arange, bernoulli_subject_k_best, color="red", linewidth = 2.0, linestyle="-", label= "Subject features, K-Best selection")
    pyplot.plot(percentil_arange, bernoulli_subject_percentile, color="red", linewidth = 2.0, linestyle="--", label= "Subject features, Percentile selection")
    pyplot.xlabel("#features")
    pyplot.ylabel("accuracy")
    pyplot.legend(loc='lower right')

    pyplot.savefig("reduce_dimensionality_bernoulli.jpg")

if __name__ == '__main__':
    plot()
