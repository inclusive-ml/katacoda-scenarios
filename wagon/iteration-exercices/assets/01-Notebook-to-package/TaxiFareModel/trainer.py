import time
import warnings

from TaxiFareModel.data import get_data, clean_df
from TaxiFareModel.utils import compute_rmse, simple_time_tracker
from sklearn.pipeline import Pipeline

warnings.filterwarnings("ignore", category=FutureWarning)


class Trainer(object):
    ESTIMATOR = "Linear"

    def __init__(self, X, y, **kwargs):
        """
        FYI:
        __init__ is called every time you instatiate Trainer
        Consider kwargs as a dict containing all possible parameters given to your constructor
        Example:
            TT = Trainer(nrows=1000, estimator="Linear")
               ==> kwargs = {"nrows": 1000,
                            "estimator": "Linear"}
        :param X: pandas DataFrame
        :param y: pandas DataFrame
        :param kwargs:
        """
        self.pipeline = None
        self.kwargs = kwargs
        self.split = self.kwargs.get("split", True)  # cf doc above
        self.X_train = X
        self.y_train = y
        # implement the rest

    def get_estimator(self):
        """Implement here"""
        return model

    def set_pipeline(self):
        """Implement here"""
        self.pipeline = Pipeline()

    @simple_time_tracker
    def train(self):
        tic = time.time()
        self.set_pipeline()
        self.pipeline.fit(self.X_train, self.y_train)

    def evaluate(self, X_test, y_test):
        if self.pipeline is None:
            raise ("Cannot evaluate an empty pipeline")
        y_pred = self.pipeline.predict(X_test)
        rmse = compute_rmse(y_pred, y_test)
        return round(rmse, 3)


if __name__ == "__main__":
    # Get and clean data
    N = 10000
    df = get_data(nrows=N)
    df = clean_df(df)
    y_train = df["fare_amount"]
    X_train = df.drop("fare_amount", axis=1)

    # Train and save model, locally and
    t = Trainer(X=X_train, y=y_train, estimator="RandomForest")
    t.train()
