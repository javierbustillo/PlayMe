import csv
from joblib import dump

import numpy
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM


def train():
    target = []
    data = []
    with open('audio_feat.csv') as data_file:
        dat = csv.reader(data_file, delimiter=',')
        for datum in dat:
            if not datum:
                continue
            split_datum = datum
            data.append([float(split) for split in split_datum[:-1]])
            target.append(split_datum[-1])

    X_train, X_test, y_train, y_test = train_test_split(numpy.array(data), numpy.array(target))
    clf = RandomForestClassifier()
    model = clf.fit(X_train, y_train)
    print('accuracy train: %f' % model.score(X_train, y_train))
    print('accuracy on test: %f' % model.score(X_test, y_test))

    dump(model, 'recommender.joblib')
