from __future__ import print_function
from __future__ import division

import pandas
import numpy
import scipy
import sklearn
import sys
import pickle
import time

from sklearn.cross_validation import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.decomposition import PCA, RandomizedPCA

from argparse import ArgumentParser

def get_features():
    features = pandas.read_csv(sys.stdin, index_col = 'num')
    X = features.drop('spam', axis = 1)
    y = features.spam
    return X.values, y.values

def profile(f, *args, **kwargs):
    time_0 = time.clock()
    ret = f(*args, **kwargs)
    time_1 = time.clock()

    return ret, time_1 - time_0

def scores_predictor(c):
    if getattr(c, 'predict_proba', None):
        categ_proba, predict_time = profile(c.predict_proba, X_test)
        y_pred = categ_proba.argmax(axis = 1)

        auc = sklearn.metrics.roc_auc_score(y_test, categ_proba[:, 1])
    else:
        y_pred, predict_time = profile(c.predict, X_test)
        auc = numpy.nan

    accuracy = (y_pred == y_test).mean()
    precision = sklearn.metrics.precision_score(y_test, y_pred)
    recall = sklearn.metrics.recall_score(y_test, y_pred)
    f1_score = sklearn.metrics.f1_score(y_test, y_pred)

    return pandas.DataFrame.from_items([
        ('accuracy', [accuracy]),
        ('auc', [auc]),
        ('precision', [precision]),
        ('recall', [recall]),
        ('f1_score', [f1_score]),
        ('predict_time_s', [predict_time]),
    ])


def parse_args():
    parser = ArgumentParser(
        description = 'Experiment with certain estimators.',
    )
    parser.add_argument('-p', '--pca', type = file, help = 'Pickle file with PCA object')
    parser.add_argument('estimator_files', type = file, nargs = '*', help = 'Pickle files with already trained estimators')
    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    estimators = map(pickle.load, args.estimator_files)

    print('Tomando features', file = sys.stderr)
    X, y = get_features()

    if args.pca:
        print('Aplicando PCA', file = sys.stderr)
        pca = pickle.load(args.pca)
        X = pca.transform(X)

    print('Calculando predicciones', file = sys.stderr)
    for e, (n, c) in enumerate(zip(args.estimator_files, estimator_files)):
        df = scores_predictor(c)
        pandas.concat(
            [
                pandas.DataFrame({'estimator': [n]}),
                df,
            ], axis = 1
        ).to_csv(sys.stdout, header = e == 0, index = False)

if __name__ == '__main__':
    main()
