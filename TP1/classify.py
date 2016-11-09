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

def parse_args():
    parser = ArgumentParser(
        description = 'Experiment with certain estimators.',
    )
    parser.add_argument('-p', '--pca', type = file, help = 'Pickle file with PCA object')
    parser.add_argument('estimator_file', type = file, help = 'Pickle file with already trained estimators')
    args = parser.parse_args()

    return args

def main():
    args = parse_args()
    estimator = pickle.load(args.estimator_file)

    print('Tomando features', file = sys.stderr)
    X = pandas.read_csv(sys.stdin, index_col = 'num').drop('spam', axis = 1).values

    if args.pca:
        print('Aplicando PCA', file = sys.stderr)
        pca = pickle.load(args.pca)
        X = pca.transform(X)

    print('Clasificando', file = sys.stderr)
    pandas.Series(
        numpy.where(estimator.predict(X), 'spam', 'ham')
    ).to_csv(sys.stdout, index = False, header = False)

if __name__ == '__main__':
    main()
