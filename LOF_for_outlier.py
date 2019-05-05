# -*- coding: utf-8 -*-
#!/usr/bin/env python
# File : test_LOF.py
# Date : 2019/5/5
# Author: leichao
# Email : leichaocn@163.com

"""简述功能.

详细描述.
原文链接为：https://www.csuldw.com/2019/03/24/2019-03-24-anomaly-detection-introduction/
数据下载地址为：https://storage.googleapis.com/kaggle-datasets/310/23498/creditcardfraud.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1557307038&Signature=ZMUhBHO4Cz9IZ4rlOBdIvQ5QN8MpJUn7Z3tYtWdZkcTjywe5%2BiRC88kq6yAvH%2BcdM%2BN141SOkVWK%2FPDTlf55zojytwMu684ldoAIJCD2%2Fkuy7cZRZuD6QXULBUyK5tSshtqbH1EBjYRuW%2FT5VPYUO5ESCUvaHIT%2BB31g443Le6pr9kKoyOrj%2F10nH7YFQ%2Fd0mzf%2FgY8WvxWlHyO7zJfNbbTIzW3kfH2WO91Y3wtKG8FIlYWyru2adVMNoCMDP%2FMV7YHeNeYV3V%2B4BXJ65lhlN4dkTjHybSzphzHd6uy8dtHoS1DtxGMHQWQRdCjH%2BfIE9vtRips%2F%2FqSwcu8DuuuUJw%3D%3D
"""

__filename__ = "test_LOF.py"
__date__ = 2019 / 5 / 5
__author__ = "leichao"
__email__ = "leichaocn@163.com"

import os
import sys

import pandas as pd
import numpy as np


creditcard_data = pd.read_csv("E:\datasets\creditcard.csv")
creditcard_data=creditcard_data.head(10000)
print(creditcard_data.head(5))

from sklearn.metrics import classification_report, accuracy_score
from sklearn.neighbors import LocalOutlierFactor

state = np.random.RandomState(42)
columns = creditcard_data.columns.tolist()
columns = [c for c in columns if c not in ["Class"]]
target = "Class"
state = np.random.RandomState(42)
X = creditcard_data[columns]
Y = creditcard_data[target]
X_outliers = state.uniform(low=0, high=1, size=(X.shape[0], X.shape[1]))

classifiers = {
    "Local Outlier Factor": LocalOutlierFactor(n_neighbors=20, algorithm='auto',
                                               leaf_size=30, metric='minkowski',
                                               p=2, metric_params=None,
                                               contamination=0.01)
}


def train_model(clf, train_X):
    # Fit the train data and find outliers
    y_pred = clf.fit_predict(X)
    scores_prediction = clf.negative_outlier_factor_
    return y_pred, clf


y_pred, clf = train_model(clf=classifiers["Local Outlier Factor"], train_X=X)


def evaluation_model(y_pred, y_label, clf_name):
    '''
    y_pred: prediction label
    y_label: true lable
    clf_name: string
    '''
    # transform anomaly label
    y_rebuild = [0 if y == 1 else 1 for y in y_pred]
    n_errors = (y_rebuild != Y).sum()

    # Classification Metrics
    print("{}: {}".format(clf_name, n_errors))
    print("Accuracy Score :", accuracy_score(Y, y_rebuild))
    print("Classification Report :")
    print(classification_report(Y, y_rebuild))


s = y_pred
evaluation_model(y_pred, Y, clf_name="LOF")
