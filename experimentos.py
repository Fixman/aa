from __future__ import print_function
from __future__ import division

import pandas
import numpy
import scipy
import sklearn
import sys
import resource
import time

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

def profile(f, *args, **kwargs):
    time_0 = time.clock()
    ret = f(*args, **kwargs)
    time_1 = time.clock

    return ret, time_1 - time_0

def score_fold(c, X_train, X_test, y_train, y_test):
    _, fit_time = profile(c.fit, X_train, y_train)

    categ_proba, predict_time = profile(c.predict_proba, X_test)
    y_pred = categ_proba.argmax(axis = 1)

    accuracy = (y_pred == y_test).mean()
    auc = sklearn.metrics.roc_auc_score(y_test, categ_proba)

    return accuracy, auc, fit_time, predict_time

def score_classifier(c, X, y, folds):
    name = c.__class__.__name__

def main():
    classifiers = [
        DecisionTreeClassifier(max_features = 'sqrt', max_height = 10, random_state = 0),
        # BernoulliNB(alpha = 1),
        # KNeighborsClassifier(5, weights = 'uniform'),
        # LinearSVC(C = 10, dual = False, random_state = 0),
    ]
    folds = StratifiedKfold(y)
    X, y = get_features()

    for e, c in enumerate(classifiers):
        feature = score_classifier(c, X, y, folds)
        feature.to_csv(sys.stdout, index = False, header = e == 0)

if __name__ == '__main__':
    main()
