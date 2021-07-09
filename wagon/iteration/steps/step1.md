
Make sure mlflow is installed.

```
pip install mlflow
```{{execute}}

```
ipython
```{{execute}}


Let's declare an experiment

```
from  mlflow.tracking import MlflowClient

EXPERIMENT_NAME = "model_experiment"

client = MlflowClient()

experiment_id = client.create_experiment(EXPERIMENT_NAME)
```{{copy}}


Let's replace "model_experiment" with "taxifare model"

```
taxifare model
```{{copy}}

If part of a time, you porobably want to qualify it a bit more but for now, it will do.

```
run_ids =  dict()
for model in ["linear", "Randomforest"]:
  run = client.create_run(experiment_id)
  run_ids[model] = run.info.run_id

client.log_param(run_ids["linear"], "model", "linear")
client.log_metric(run_ids["linear"], "rmse", 4.5)
```{{copy}}


We can log more parameters

```
client.log_param(run_ids["linear"], "hyperparameters 1", "abc")
client.log_param(run_ids["linear"], "hyperparameters 2", 3.5)
```{{copy}}

The hyperparameters are usually not the same for all models. Let's also create one for the "RandomForest" model.

```
client.log_param(run_ids["Randomforest"], "hyperparameters 3", 1.3)
```{{copy}}


## MLFlow admin interface

```
mlflow ui
```{{execute T2}}


Console

```
[2020-06-06 10:46:51 +0200][4980] [INFO] Starting gunicorn 20.0.4
[2020-06-06 10:46:51 +0200][4980] [INFO] Listening at: http://127.0.0.1:5000 (4980)
[2020-06-06 10:46:51 +0200][4980] [INFO] Using worker: sync
[2020-06-06 10:46:51 +0200][4983] [INFO] Booting worker with pid: 4983
```

In order to see the results of the tracking, go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Detour if on Katacoda

Within the Katacoda environment, it's slightly different

```
https://[[HOST_SUBDOMAIN]]-5000-[[KATACODA_HOST]].environments.katacoda.com/
```{{copy}}

Alternatively, tunnel to a public address. For this, let's install `ngrok` in a new terminal window:

```
curl https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip -o ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
```{{execute T3}}

```
./ngrok http 5000
```{{execute T3}}


## Back to MLFlow

Ok, let's check our runs.

If we want details, we can choose the compare functionality. At the bottom, graphs that let us check the evolution of performance across runs.

Quite simple.

## Files created

```
tree mlruns -L 2
```{{execute T4}}

```
tree mlruns
```{{execute T4}}

```
cat mlruns/2/{run_id}/params/model
```{{copy}}

## Working in a team

### Using MLflow hosted on a server

For instance: [https://mlflow-dev.herokuapp.com/#/](https://mlflow-dev.herokuapp.com/#/)

=> equivalent of you connecting via my ngrok url. Something like this (it will change at each session).

```
http://9b25dc42c618.ngrok.io
```


