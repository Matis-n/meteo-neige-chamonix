import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedGroupKFold

import rampwf as rw

problem_title = "Verglas prediction from meteorological data"



# Mapping categories to int

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
    #
    # returns X (input) and y (output) arrays


    data_df = pd.read_csv(os.path.join(path, "data", split + ".csv"))

    data_df["SampleID"] = data_df["SampleID"].astype("category")
    SampleID = np.array(data_df["SampleID"].cat.codes)

    # Retrieve the geochemical data for X.
    # FeO, Fe2O3 and FeO2O3T are dropped because FeOT
    # is a different expression of the same element (Fe).
    # P2O5 and Cl are also dropped because they are sporadically analyzed.
    

    
    X_df = data_df.loc[:, majors + traces ]# + ["AnalyticalTechnique", "TypeOfSection"]]

    X_df["groups"] = SampleID.tolist()

    X = X_df

    # labels
    y = np.array(data_df["Event"].map(cat_to_int).fillna(-1).astype("int8"))

    return X, y


groups = None


# Here we will define a global variable (groups) to be used in get_cv
# for the SGKF CV strategy
def get_train_data(path="."):
    data = pd.read_csv(os.path.join(path, "data", "train.csv"))
    data_df = data.copy()
    data_df["SampleID"] = data_df["SampleID"].astype("category")
    SampleID = np.array(data_df["SampleID"].cat.codes)
    global groups
    groups = SampleID
    return _get_data(path, "train")


def get_test_data(path="."):
    return _get_data(path, "test")


def get_cv(X, y):
    # groups = get_groups()
    cv = StratifiedGroupKFold(n_splits=2, shuffle=True, random_state=2)
    return cv.split(X, y, groups)

def preprocess(X):
    # This is the preprocess function for the data.
    # It is called after loading the data and before training the model.
    # It should return the modified data.

    return X
