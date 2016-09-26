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
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, FunctionTransformer

def get_features():
    features = pandas.read_csv(sys.stdin)
    X = features.drop('spam', axis = 1)
    y = features.spam
    return X.values, y.values

def profile(f, *args, **kwargs):
    time_0 = time.clock()
    ret = f(*args, **kwargs)
    time_1 = time.clock()

    return ret, time_1 - time_0

def score_fold(c, X_train, X_test, y_train, y_test):
    _, fit_time = profile(c.fit, X_train, y_train)

    if getattr(c, 'predict_proba', None):
        categ_proba, predict_time = profile(c.predict_proba, X_test)
        y_pred = categ_proba.argmax(axis = 1)

        accuracy = (y_pred == y_test).mean()
        auc = sklearn.metrics.roc_auc_score(y_test, categ_proba[:, 1])
    else:
        accuracy, predict_time = profile(c.score, X_test, y_test)
        auc = numpy.nan

    return accuracy, auc, fit_time, predict_time

def score_classifier(c, X, y, folds):
    scores = []
    for train, test in folds:
        scores.append(score_fold(c, X[train], X[test], y[train], y[test]))

    accuracy, auc, fit_time, predict_time = numpy.array(scores).mean(axis = 0)
    return pandas.DataFrame.from_items([
        ('accuracy', [accuracy]),
        ('auc', [auc]),
        ('fit_time_s', [fit_time]),
        ('predict_time_s', [predict_time]),
    ])

def main():
    resource.setrlimit(resource.RLIMIT_AS, (6e9, 6e9))

    normalizers = [
        ('id', FunctionTransformer()),
        ('scale', StandardScaler()),
        # ('logarithmic', Pipeline([('log1p', FunctionTransformer(numpy.log1p)), ('scale', StandardScaler())])),
    ]
    classifiers = [
        BernoulliNB(alpha = 1, fit_prior = True),
        DecisionTreeClassifier(max_features = 'sqrt', max_depth = 10, random_state = 0),
        KNeighborsClassifier(5, weights = 'uniform'),
        LinearSVC(C = 10, dual = False, random_state = 0),
    ]
    X, y = get_features()
    folds = StratifiedKFold(y, n_folds = 10, random_state = 1)

    first = True
    for norm_name, n in normalizers:
        for c in classifiers:
            data = pandas.DataFrame.from_items([
                ('normalizacion', [norm_name],),
                ('clasificador', [c.__class__.__name__])
            ])

            feature = pandas.concat(
                [
                    data,
                    score_classifier(Pipeline([('norm', n), ('classify', c)]), X, y, folds),
                ],
                axis = 1
            )

            feature.to_csv(sys.stdout, index = False, header = first)
            first = False

if __name__ == '__main__':
    main()
