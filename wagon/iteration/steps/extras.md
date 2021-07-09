````
pip install category_encoders
pip install pygeohash
pip install memoized_property
clear
````

```
mkdir mlflow && cd mlflow
touch localhost.py
python localhost.py
```{{execute}}

```python
import mlflow
from  mlflow.tracking import MlflowClient
mlflow.set_tracking_uri("{mlflow_server}")
EXPERIMENT_NAME = "[team_identifier] [login] problem name + version"
```{{copy}}

```python
client = MlflowClient()
experiment_id = client.create_experiment(EXPERIMENT_NAME)

run_ids =  dict()
for model in ["linear", "Randomforest"]:
  run = client.create_run(experiment_id)
  run_ids[model] = run.info.run_id

client.log_param(run_ids["linear"], "model", "linear")
client.log_metric(run_ids["linear"], "rmse", 4.5)
```


---

```python
import mlflow
from mlflow.tracking import MlflowClient

# MLFLOW_URI = "http://127.0.0.1:5000"
MLFLOW_URI = "http://f510c1729635.ngrok.io"

myname="widged"
EXPERIMENT_NAME = f"TaxifareModel_{myname}"
mlflow.set_tracking_uri(MLFLOW_URI)
mlflow_client= MlflowClient()

experiment_id = 0
# Create the resource.
# If exception is raised because a resource of that name already exists
#      mlflow.exceptions.RestException: RESOURCE_ALREADY_EXISTS: Experiment 'TaxifareModel_widged' already exists.
# recover the id of the experiment of that name
try:
    experiment_id = mlflow_client.create_experiment(EXPERIMENT_NAME)
except BaseException:
    experiment_id = mlflow_client.get_experiment_by_name(EXPERIMENT_NAME).experiment_id

print(experiment_id)

for model in ["linear", "Randomforest"]:
    run = mlflow_client.create_run(experiment_id)
    mlflow_client.log_metric(run.info.run_id, "rmse", 1.5)
    mlflow_client.log_param(run.info.run_id, "model", model)

```{{copy}}





# 2. Running it on a shared host

```
touch sharedhost.py
python sharedhost.py
```{{execute}}

MLflow server: [ngrok](ngrok)


```python

mlflow.set_tracking_uri("{ngrokurl}")
EXPERIMENT_NAME = "[BE] [Belgium] [widged] TaxifareModel_0.01"
mlflow_client= MlflowClient()

```{{copy}}


