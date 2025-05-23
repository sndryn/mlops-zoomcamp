# 02 - Experiment Tracking

Glossary

| Term | Definition |
|------|------|
| ML Experiment | Process of building ML model |
| Experiment run | Each trial in an ML Experiment |
| Run artifact | Any file tha is associated with an ML run |
| Experiment metadata | information related to experiment |

### Experiment Tracking

Process of keepign track of all relevant infromation (e.g. source code, environment, data, model, hyperparameters, metrics) from an ML experiment

Reasons: reproducability, organization, optimization

### ML Flow

Open source for ML lifecycle

Modules: 
- Tracking:
    - organize experiments into runs
    - keep track of parameters, metrics, metadata, artifacts, models
    - log: source code, version of the code (git commit), start and end time, author
- Models
- Model registry
- Projects


#### Installing MLFLow and Launching ML Flow UI

1. Install requirements.txt
2. Check mlflow availability via CLI
3. Run mlflow UI
```
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
4. Open `http://127.0.0.1:5000`

#### mlflow Python Library

1. To set tracking in Python
```
import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nyc-taxi-experiment") # experiment name
```
2. Run MLFlow run
```
with mlflow.start_run():
    ...
```
3. Set tag: `mlflow.set_tag("<key>", "<value>")`
4. Log param: `mlflow.log_param("<key>", "<value>")`
5. Log metric: `mlflow.log_metric("<metric name>", <value>)`
6. Autolog: `mlflow.<framework>.autolog()` (example for xgboost)
7. Store model: `mlflow.log_artifact(local_path=, artifact_path=)`
8. Store model (framework): `mlflow.<framework>.log_model(<model>, artifact_path=)`
9. Load model as Python function: `mlflow.pyfunc.load_model(<path>)`
10. Load model as the particular framework: `mlflow.<framework>.load_model(<path>)`

#### Model Management

Machine Learning Lifecycle (including model management)
![Alt text](<image/machine_learning_lifecycle.png>)

### Model Registry
![Alt text](<image/model registry.png>)

How to regsiter the model via UI:
1. Go to the UI
2. Click one of the experiment run
3. Go to the artifacts and click models_mlflow
4. Click the button `Register Model`
5. Create New Model if no model created, write the name of the model and click OK
![Alt text](<image/register_model.png>)
6. Go to menu Models to see registered models

Notes:
MLflow stages feature in page registered models is deprecated in the new version. See [this reference](<https://mlflow.org/docs/latest/model-registry#deprecated-using-model-stages>)

- model lineage
- model versioning
- stage transitions
- annotations


How to register model via Python SDK:
```
run_id = "<run id>" 
model_uri = f"runs:/{run_id}/model"

mlflow.register_model(model_uri=model_uri, 
                      name="nyc-taxi-model")
```

MLflowClient Class
- A client of mlflow tracking server to create and manage experiments and runs
- A client of mlflow registry server to create and amange registered models and versioning

```
from mlflow.tracking import MlflowClient

MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"

client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
```



### MLFlow Practice
Scenario
1. 1 DS
2. Cross-functional team with 1 DS
3. Multiple DS


Configuring MLFlow
1. Backend Store: local file system, SQLAlchemy compatible DB
2. Artifact store: local file system, Remote (e.g. s3 Bucket)
3. Tracking server: no server, localhost, remote host

### Best practice
1. Remote tracking server
- easily deployed to the cloud
- Share experiments with other DS
- Collaborate to build and deploy models
- Give more visibility of the DS efforts