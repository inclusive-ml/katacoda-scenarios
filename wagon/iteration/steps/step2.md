
Simply creating the class doing nothing for now.

```
ipython
```{{execute}}

```
# no copy/paste

class Trainer(object):

  def __init__(self, X, y, **kwargs):
      self.pipeline = None
      self.kwargs = kwargs
      self.dist = self.kwargs.get("distance_type", "euclidian")
      self.X_train, self.X_val, self.y_train, self.y_val = \
          train_test_split(X, y, test_size=0.15)
      self.nrows = self.X_train.shape[0]

  def get_estimator(self):
      estimator = self.kwargs.get("estimator", "RandomForest")
      if estimator == "RandomForest":
          model = RandomForestRegressor()
      return model
```

What I want

````python
params = dict([
  ('model', 'regression'),
  ('hyper_param1', 'abc'),
  ('hyper_param2', 123),
  ('nrows', 1_000_000),
  ('pipeline_add_distance', True)
])
params
```{{copy}}

Instantiate the trainer

```python
trainer = Trainer(X_train, y_train, **params)
```

`**` for unpacking. Equivalent to `model="regression", hyper_param1="abc", hyper_param2=123)`

```python
trainer.fit() # -> send params to mlflow
trainer.evaluate_perf() # -> push metrics to mlflow
```

Then we can define several trainers

```
trainers =  [
  {
    'estimator': 'regression',
    'hyper_param1':'abc',
    'hyper_param2':123,
    'nrows':1_000_000,
    'pipeline_add_distance': True,
    'pipeline_add_d2center': True,
    'pipeline_add_pickuptime', True
  },
  {
    'estimator':'randomforest',
    'hyper_param1':'def',
    'hyper_param3':456,
    'nrows':100_000_000,
    'pipeline_add_distance': False,
    'pipeline_add_d2center': True,
    'pipeline_add_pickuptime', False
  }
]
```{{copy}}

Let's loop

```
for params in trainers:
  trainer = Trainer(X_train, y_train, **params)
  trainer.fit() # -> send params to mlflow
  trainer.evaluate_perf() # -> push metrics to mlflow
```

Let's add a pipeline to the trainer

```
  def set_pipeline(self):
      # Define feature engineering pipeline blocks here
      pipe_tf = make_pipeline(TimeEncoder(),
                              OneHotEncoder())
      pipe_dist = make_pipeline(DistTransformer(distance_type=self.dist),
                                    StandardScaler())
      pipe_d2center = make_pipeline(DistToCenter(),
                                    StandardScaler())
      # Define default feature engineering blocs
      distance_columns = list(DIST_ARGS.values())
      feateng_blocks = [
          ('distance', pipe_dist, distance_columns),
          ('time_features', pipe_tf, ['pickup_datetime']),
          ('distance_to_center', pipe_d2center, distance_columns)]
      features_encoder = ColumnTransformer(feateng_blocks,
                                           n_jobs=None,
                                           remainder="drop")
      regressor = self.get_estimator()
      self.pipeline = Pipeline(steps=[
                  ('features', features_encoder),
                  ('rgs', regressor)])

```

Pipeline with two steps (1) features_encoder, (2) regressor.

"regressor" we do not specify a precise model as we want the class to be fairly generic. We delegate to `get_estimator()`


```
  def get_estimator(self):
      estimator = self.kwargs.get("estimator", "RandomForest")
      if estimator == "RandomForest":
          model = RandomForestRegressor()
      elif estimator == "XGBoost":
          model = XGBoostRegressor()
      return model

```

Now the code for the training

```
  def train(self):
      self.set_pipeline()
      self.pipeline.fit(self.X_train, self.y_train)

  def evaluate(self):
      rmse_train = self.compute_rmse(self.X_train, self.y_train)
      rmse_val = self.compute_rmse(self.X_val, self.y_val, show=True)
      output_print = f"rmse train: {rmse_train} || rmse val: {rmse_val}"
      print(colored(output_print, "blue"))

  def compute_rmse(self, X_test, y_test, show=False):
      y_pred = self.pipeline.predict(X_test)
      rmse = compute_rmse(y_pred, y_test)
      return round(rmse, 3)

  def save_model(self):
      """Save the model into a .joblib format"""
      joblib.dump(self.pipeline, 'model.joblib')
      print(colored("model.joblib saved locally", "green"))
```

"# Define feature engineering pipeline blocks here". We can make some aspects of pipeline execution conditional on the basis of the parameters injected.

```
  def set_pipeline(self):

    feateng_blocks = []
    if self.kwargs.get('pipeline_add_distance', True):
      pipe = make_pipeline(
        DistTransformer(distance_type=self.dist), StandardScaler()
      )
      feateng_blocks.append(('distance', pipe, distance_columns))
```

```
    if self.kwargs.get('pipeline_add_pickuptime', True):
      pipe = make_pipeline(
        TimeEncoder(),
        OneHotEncoder()
      )
      feateng_blocks.append(('time_features', pipe, ['pickup_datetime']))
```

```
    if self.kwargs.get('pipeline_add_d2center', True):
      pipe = make_pipeline(
        DistToCenter(),
        StandardScaler()
      )
      feateng_blocks.append(('distance_to_center', pipe_d2center, distance_columns))
```

Then we have a call to fit for the training phase

```
    def train(self):
        self.set_pipeline()
        self.pipeline.fit(self.X_train, self.y_train)
```

And finally we have a call to evaluate for the validation phase

```
  def evaluate(self):
    if estimator == "RandomForest":
      rmse_train = self.compute_rmse(self.X_train, self.y_train)
      rmse_val = self.compute_rmse(self.X_val, self.y_val, show=True)
      output_print = f"rmse train: {rmse_train} || rmse val: {rmse_val}"
      print(colored(output_print, "blue"))
    elif estimator == "XGBoost":
      # do something else
    return model
```

Et une méthode pour sauver le modèle

```
  def save_model(self):
      """Save the model into a .joblib format"""
      joblib.dump(self.pipeline, 'model.joblib')
      print(colored("model.joblib saved locally", "green"))
```


You have the choice. Writing trainers that are very generic. Or write a number of customer trainers.
