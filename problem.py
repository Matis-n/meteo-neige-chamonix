import os
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
import rampwf as rw

problem_title = "Snow prediction from meteorological data"


Predictions = rw.prediction_types.make_multiclass(label_names=[0, 1])
workflow = rw.workflows.Classifier()


score_types = [
    rw.score_types.BalancedAccuracy(
        name="bal_acc", precision=3, adjusted=False
    ),
    rw.score_types.Accuracy(name="acc", precision=3),
]

def _get_data(path=".", split="train"):
    # Load data from csv files into pd.DataFrame
    # returns X (input) and y (output) arrays

    # read train or test data
    data = pd.read_csv(os.path.join(path, "data", split + ".csv"), sep=";", decimal=".")
    # preprocess
    # numerical and categorical columns
    num_cols = data.select_dtypes(include=np.number).columns
    cat_cols = data.select_dtypes(include='object').columns

    # keep date column
    # cat_cols = cat_cols.drop('AAAAMMJJ')
    # throw away categorical columns
    data = data.drop(columns=cat_cols)
    data = data.drop(columns=['NUM_POSTE'])

    y_target = 'NEIG'
    # columns with NEIG in name
    y_covariates = [col for col in data.columns if 'NEIG' in col]
    X = data.drop(columns=y_covariates)
    #labels
    y = data[y_target].astype('int8')
    return X, y

def get_train_data(path="."):
    return _get_data(path, "train")


def get_test_data(path="."):
    return _get_data(path, "test")


def get_cv(X, y):
    cv = KFold(n_splits=2, shuffle=True, random_state=2)
    return cv.split(X, y)


