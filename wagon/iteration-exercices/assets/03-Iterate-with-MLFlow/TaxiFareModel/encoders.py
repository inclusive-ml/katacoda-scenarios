import pandas as pd
import pygeohash as gh
from TaxiFareModel.data import get_data, clean_df, DIST_ARGS
from TaxiFareModel.utils import haversine_vectorized, minkowski_distance
from sklearn.base import BaseEstimator, TransformerMixin


class TimeFeaturesEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, time_column, time_zone_name='America/New_York'):
        self.time_column = time_column
        self.time_zone_name = time_zone_name

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X.index = pd.to_datetime(X[self.time_column])
        X.index = X.index.tz_convert(self.time_zone_name)
        X["dow"] = X.index.weekday
        X["hour"] = X.index.hour
        X["month"] = X.index.month
        X["year"] = X.index.year
        return X[["dow", "hour", "month", "year"]].reset_index(drop=True)

    def fit(self, X, y=None):
        return self


class AddGeohash(BaseEstimator, TransformerMixin):

    def __init__(self, precision=6):
        self.precision = precision

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        X['geohash_pickup'] = X.apply(
            lambda x: gh.encode(x.pickup_latitude, x.pickup_longitude, precision=self.precision), axis=1)
        X['geohash_dropoff'] = X.apply(
            lambda x: gh.encode(x.dropoff_latitude, x.dropoff_longitude, precision=self.precision), axis=1)
        return X[['geohash_pickup', 'geohash_dropoff']]


class DistanceTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, distance_type="haversine"):
        self.distance_type = distance_type

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        if self.distance_type == "haversine":
            X["distance"] = haversine_vectorized(X, **DIST_ARGS)
        if self.distance_type == "euclidian":
            X["distance"] = minkowski_distance()
        return X[["distance"]]

    def fit(self, X, y=None):
        return self



if __name__ == "__main__":
    params = dict(nrows=1000,
                  upload=False,
                  local=False,  # set to False to get data from GCP (Storage or BigQuery)
                  optimize=False)
    df = get_data(**params)
    df = clean_df(df)
    dist = DistanceTransformer()
    X = dist.transform(df)
