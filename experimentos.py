from __future__ import print_function
from __future__ import division

import pandas
import numpy
import scipy
import sklearn
import sys
import resource

from sklearn.cross_validation import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC

def get_features():
    features = pandas.read_csv(sys.stdin)
    X = features.drop('spam', axis = 1)
    y = features.spam
    return X, y

def score_classifier(c, X, y):
    name = c.__class__.__name__

def main():
    classifiers = [
        DecisionTreeClassifier(max_features = 'sqrt', max_height = 10, random_state = 0),
        # BernoulliNB(alpha = 1),
        # KNeighborsClassifier(5, weights = 'uniform'),
        # LinearSVC(C = 10, dual = False, random_state = 0),
    ]
    X, y = get_features()

    for e, c in enumerate(classifiers):
        feature = score_classifier(c)
        feature.to_csv(sys.stdout, index = False, header = e == 0)

if __name__ == '__main__':
    main()
