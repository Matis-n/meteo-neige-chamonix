from sklearn.base import BaseEstimator
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier


class Classifier(BaseEstimator):
    def __init__(self):
        self.transformer = Pipeline(
            steps=[("scaler", MinMaxScaler())]
        )
        self.model = XGBClassifier()
        self.pipe = make_pipeline(self.transformer, self.model)

    def fit(self, X, y):
        self.pipe.fit(X, y)

    def predict(self, X):
        return self.pipe.predict(X)
    
    def predict_proba(self, X):
        return self.pipe.predict_proba(X)
