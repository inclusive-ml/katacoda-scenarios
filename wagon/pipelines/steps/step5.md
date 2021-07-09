
## Commençons avec un nouvel environnement

```
ipython
```{{execute}}

## Applied to the whole dataframe

```
import pandas as pd
```{{copy}}


```
from sklearn.base import BaseEstimator, TransformerMixin

class HourTransformer(BaseEstimator, TransformerMixin):

  def __init__(self, time_column, time_zone_name='America/Los_Angeles'):
      self.time_column = time_column
      self.time_zone_name = time_zone_name

  def fit(self, X, y=None):
      return self

  def transform(self, X, y=None):
      assert isinstance(X, pd.DataFrame)

      X.index = pd.to_datetime(X[self.time_column])
      X.index = X.index.tz_convert(self.time_zone_name)
      X["hour"] = X.index.hour
      return X[["hour"]].reset_index(drop=True)
```{{copy}}




This will extract a single from the whole dataset feature to be used for training.

```
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

custom_pipe = Pipeline(steps=[
    ('time_features', HourTransformer( time_column='pickup_datetime',
                                    time_zone_name='America/Los_Angeles')),
    ('scaler', StandardScaler()),
    ('regressor', RandomForestRegressor())])
```{{copy}}

```
df = pd.read_csv('https://clients.widged.com/wagon/data/taxi-fare-train.csv', nrows=100 )
X = df.drop('fare_amount', axis=1)
y = df['fare_amount']
```{{copy}}

```
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1, random_state=42)
X_train.shape, y_train.shape, X_test.shape , y_test.shape
```{{copy}}


```
custom_pipe.fit(X_train, y_train)
custom_pipe.predict(X_test)
```{{copy}}

## Applied only to certain columns

HourTransformer

```
class HourTransformer(BaseEstimator, TransformerMixin):

  def __init__(self, time_column, time_zone_name='America/Los_Angeles'):
      self.time_column = time_column
      self.time_zone_name = time_zone_name

  def fit(self, X, y=None):
      return self

  def transform(self, X, y=None):
      assert isinstance(X, pd.DataFrame)

      X.index = pd.to_datetime(X[self.time_column])
      X.index = X.index.tz_convert(self.time_zone_name)
      X["hour"] = X.index.hour
      return X[[
              'hour',
          ]].reset_index(drop=True)
```{{copy}}

DistanceTransformer

```
def minkowski_distance(start,end, p):
  (x1, y1) = start
  (x2, y2) = end
  return ((abs(x2 - x1) ** p) + (abs(y2 - y1)) ** p) ** (1 / p)

```{{copy}}


```
class DistanceTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        assert isinstance(X, pd.DataFrame)
        x1, y1 = X["pickup_longitude"], X["pickup_latitude"]
        x2, y2 = X["dropoff_longitude"], X["dropoff_latitude"]
        X['distance'] = minkowski_distance((x1, y1),(x2, y2), p=1)
        return X[[
                'distance',
            ]]
```{{copy}}




I can now create a number of new features derived from my dataset, here time and distance.

```
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
```{{copy}}

```
pipe_time = make_pipeline(HourTransformer(time_column='pickup_datetime'), StandardScaler())
pipe_time
```{{copy}}

```
pipe_distance = make_pipeline(DistanceTransformer(), RobustScaler())
pipe_distance
```{{copy}}

Deux pipelines

```
dist_cols = ['pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude']
time_cols = ['pickup_datetime']

feat_eng = ColumnTransformer([
  ('time', pipe_time, time_cols),
  ('distance', pipe_distance, dist_cols)])
  # remainder='passthrough' # This would keep the other columns
```{{copy}}

**Note**

```
pipe_time = make_pipeline(
  HourTransformer(time_column='pickup_datetime'),
  StandardScaler())
pipe_time
```

is exactly the same as

```
pipe_time = Pipeline(steps=[
  ('time_features', HourTransformer( time_column='pickup_datetime')),
  ('scaler', StandardScaler())
])
```

The first one is just more compact

The pipeline takes the whole dataset as an input and produces a new feature (column) as an output.

Étapes

```
pipe_cols = Pipeline(steps=[
  ('feat_eng', feat_eng),
  ('scaler', StandardScaler()), # should it be there?
  ('regressor', RandomForestRegressor())])

pipe_cols.fit(X_train, y_train)

Y = pipe_cols.predict(X_train)
Y
```{{copy}}


