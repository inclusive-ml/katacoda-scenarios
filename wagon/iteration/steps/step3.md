# Memoization

Persist information about the result for a (@memoized) function call and its parameters.
If there is later another call to the function with the exact same paramters, it will return the stored result without attempting to run the function again.

If any parameter is different, it will run the function and persist the association between function with parameters and result

```
ipython
```{{execute}}


```python
pip install memoized_property
```{{execute}}

## Non memoized car

```
from memoized_property import memoized_property
from random import random

class Car():
    def get_random_value(self):
        return random()
```{{copy}}

Let's create a first instance of the class
```
car = Car()
```{{copy}}

```
print('non memoized calls differ:')
print(car.get_random_value())
print(car.get_random_value())
print(car.get_random_value())
print(car.get_random_value())
```{{copy}}

Let's create a second instance of the class

```
car2 = Car()
```{{copy}}

```
print('non memoized calls differ:')
print(car2.get_random_value())
print(car2.get_random_value())
print(car2.get_random_value())
print(car2.get_random_value())
```{{copy}}

## Memoized car


```
from memoized_property import memoized_property
from random import random


class MemoizedCar():
    @memoized_property
    def get_random_value(self):
        return random()
```{{copy}}

Let's create a first instance of the class

```
car = MemoizedCar()
print('memoized property return the same value:')
print(car.get_random_value)
print(car.get_random_value)
print(car.get_random_value)
print(car.get_random_value)
```{{copy}}

Let's create a second instance of the class

```
car2 = MemoizedCar()
print('memoized property return the same value:')
print(car2.get_random_value)
print(car2.get_random_value)
print(car2.get_random_value)
print(car2.get_random_value)

```{{copy}}

## Manually  persisting value across calls

Singleton Pattern

```
class SingletonCar():

  def __init__(self):
    self.random_value = None

  def get_random_value(self):
    #if not hasattr(self, 'random'):
    if self.random_value == None:
      self.random_value = random()
    return self.random_value

print('----singleton pattern----')
car = SingletonCar()
print('all calls return the same value:')
print(car.get_random_value())
print(car.get_random_value())

car2 = SingletonCar()
print('all calls return the same value:')
print(car2.get_random_value())
print(car2.get_random_value())
```{{copy}}


## All together! Memoized trainer

```
export MLFLOW_URI={ngrok-url}
```{{copy}}


```
ipython
```{{execute}}


```
from memoized_property import memoized_property

import os
import mlflow
from mlflow.tracking import MlflowClient

class Trainer():

  def __init__(self, experiment_name, mlflow_uri):
    self.experiment_name = experiment_name
    self.mlflow_uri = mlflow_uri

  @memoized_property
  def mlflow_client(self):
    mlflow.set_tracking_uri(self.mlflow_uri)
    return MlflowClient()

  @memoized_property
  def mlflow_experiment_id(self):
    try:
        return self.mlflow_client \
            .create_experiment(self.experiment_name)
    except BaseException:
        return self.mlflow_client \
            .get_experiment_by_name(self.experiment_name).experiment_id

  def mlflow_create_run(self):
    self.mlflow_run = self.mlflow_client \
          .create_run(self.mlflow_experiment_id)

  def mlflow_log_param(self, key, value):
    self.mlflow_client \
          .log_param(self.mlflow_run.info.run_id, key, value)

  def mlflow_log_metric(self, key, value):
    self.mlflow_client \
          .log_metric(self.mlflow_run.info.run_id, key, value)

  def train(self):
    for model in ["linear", "Randomforest"]:
        self.mlflow_create_run()
        self.mlflow_log_metric("rmse", 4.5)
        self.mlflow_log_param("model", model)
```{{copy}}

Now let's run an experiment

```
MLFLOW_URI = "https://user:PASSWORD@mlflow-dev.herokuapp.com/"
trainer = Trainer("[BE][bruxelles] DE D3 model_experiment 6", MLFLOW_URI)
trainer.train()
```{{copy}}

## Better way to write code

```
from memoized_property import memoized_property

import os
import mlflow
from mlflow.tracking import MlflowClient

class MlFlowTracker():

  def __init__(self, experiment_name, mlflow_uri):
    self.experiment_name = experiment_name
    self.mlflow_uri = mlflow_uri

  @memoized_property
  def mlflow_client(self):
    mlflow.set_tracking_uri(self.mlflow_uri)
    return MlflowClient()

  @memoized_property
  def mlflow_experiment_id(self):
    try:
        return self.mlflow_client \
            .create_experiment(self.experiment_name)
    except BaseException:
        return self.mlflow_client \
            .get_experiment_by_name(self.experiment_name).experiment_id

  def create_run(self):
    self.mlflow_run = self.mlflow_client \
          .create_run(self.mlflow_experiment_id)

  def log_param(self, key, value):
    self.mlflow_client \
          .log_param(self.mlflow_run.info.run_id, key, value)

  def log_metric(self, key, value):
    self.mlflow_client \
          .log_metric(self.mlflow_run.info.run_id, key, value)
```{{copy}}

```
class Trainer():

  def __init__(self, experiment_name, mlflow_uri):
    self.mlf_tracker = MlFlowTracker(experiment_name, mlflow_uri)

  def train(self):
    for model in ["linear", "Randomforest"]:
        self.mlf_tracker.create_run()
        self.mlf_tracker.log_metric("rmse", 4.5)
        self.mlf_tracker.log_param("model", model)
```{{copy}}
