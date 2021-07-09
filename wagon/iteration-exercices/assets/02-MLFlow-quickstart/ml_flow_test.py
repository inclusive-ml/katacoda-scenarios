import mlflow
from  mlflow.tracking import MlflowClient
EXPERIMENT_NAME = "test_experiment"
# Indicate mlflow to log to remote server
mlflow.set_tracking_uri("{mlflow-server-url-provided-at-lecture-time}")
client = MlflowClient()
# Here experiment name already exists so we just get its existing id
experiment_id = client.get_experiment_by_name(EXPERIMENT_NAME).experiment_id

for model in ["linear", "Randomforest"]:
    run = client.create_run(experiment_id)
    client.log_metric(run.info.run_id, "rmse", 4.5)
    client.log_param(run.info.run_id, "model", model)
    client.log_param(run.info.run_id, "student_name", "jean")
