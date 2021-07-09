Install Conda

```
wget -q https://repo.continuum.io/miniconda/Miniconda3-4.5.1-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -f -b -p /opt/conda && \
    /opt/conda/bin/conda install --yes python=3.6 pip=9.0.3 && \
    rm /tmp/miniconda.sh

export PATH=/opt/conda/bin:$PATH
```{{copy}}

Install Python Libraries

```
pip install mlflow==1.7.2
pip install pandas==1.0.2
pip install keras==2.3.1
pip install tensorflow==1.14.0
pip install scikit-learn==0.22.2.post1
```{{copy}}

Install Java (for use with Spark)

```
apt-get update \
  && apt-get install -y software-properties-common \
  && add-apt-repository -y ppa:openjdk-r/ppa \
  && apt-get update \
  && apt-get install -y --no-install-recommends openjdk-8-jdk openjdk-8-jre-headless \
  && apt-get install -y --no-install-recommends apt-transport-https

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/

export PATH=/usr/lib/jvm/java-8-openjdk-amd64/jre/bin:$PATH
```{{copy}}

Start the Server
```
export MLFLOW_TRACKING_URI=file:///root/mlflow

nohup mlflow server --host 0.0.0.0 \
                    --port 5000 \
                    --backend-store-uri file:///root/mlflow &

```{{copy}}

Simple python script

```
import os
from random import random, randint

import mlflow
from mlflow import log_metric, log_param, log_artifacts

tracking_uri='file:///root/mlflow'
mlflow.set_tracking_uri(tracking_uri)

experiment_name = 'hello_world'
mlflow.set_experiment(experiment_name)

if __name__ == "__main__":
    print("Running mlflow_tracking.py")

    log_param("hyperparam1", randint(0, 100))

    log_metric("accuracy", random())
    log_metric("accuracy", random() + 1)
    log_metric("accuracy", random() + 2)

    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open("outputs/model.txt", "w") as f:
        f.write("hello world!")

    log_artifacts("outputs")
```{{copy}}

```
cd ~

git clone [https://github.com/PipelineAI/katacoda-notebooks](https://github.com/PipelineAI/katacoda-notebooks)

cd ~/katacoda-notebooks/06_mlflow_install/

python mlflow_tracking.py
```{{copy}}


