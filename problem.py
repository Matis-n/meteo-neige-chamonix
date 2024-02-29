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
    #
    # returns X (input) and y (output) arrays

    # read train or test data
    data = pd.read_csv(os.path.join(path, "data", split + ".csv"))
    # preprocess
    #columns of data
    num_cols = data.select_dtypes(include=np.number).columns
    cat_cols = data.select_dtypes(include='object').columns
    #throw away categorical columns
    data = data.drop(columns=cat_cols)
    data = data.drop(columns=['NUM_POSTE'])

    y_target = 'NEIG'
    # print columns with NEIG in name
    y_covariates = [col for col in data.columns if 'NEIG' in col]
  
    # NEIG = 0 if NEIGETOTX = 0 and 1 else
    data['NEIG'] = data['NEIG'].mask(data['NEIGETOTX'] == 0, 0)
    data['NEIG'] = data['NEIG'].mask(data['NEIGETOTX'] > 0, 1)

    data.dropna(subset=[y_target], inplace=True)

    X = data.drop(columns=y_covariates)
    #labels
    y = data[y_target].astype('int8')
    return X, y


# groups = None


# Here we will define a global variable (groups) to be used in get_cv
# for the SGKF CV strategy
def get_train_data(path="."):
    # data = pd.read_csv(os.path.join(path, "data", "train.csv"))
    # data = data.copy()
    # data["SampleID"] = data["SampleID"].astype("category")
    # SampleID = np.array(data["SampleID"].cat.codes)
    # global groups
    # groups = SampleID
    return _get_data(path, "train")


def get_test_data(path="."):
    return _get_data(path, "test")


def get_cv(X, y):
    cv = KFold(n_splits=2, shuffle=True, random_state=2)
    return cv.split(X, y)


