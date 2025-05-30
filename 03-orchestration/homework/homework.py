#!/usr/bin/env python
# coding: utf-8
# prefect 3.4.4

import pickle
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

from prefect import task, flow

import mlflow
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("nyc-taxi-experiment")

models_folder = Path('models')
models_folder.mkdir(exist_ok=True)

@task(retries=3, retry_delay_seconds=5)
def read_dataframe(year, month):
    url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet'
    df = pd.read_parquet(url)
    print(f"Number of records of Yellow taxi trips in {year}-{month:02d} = {len(df)}")

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    return df

@task(retries=1, retry_delay_seconds=5)
def create_X(df, dv=None):
    categorical = ['PULocationID', 'DOLocationID']
    dicts = df[categorical].to_dict(orient='records')

    if dv is None:
        dv = DictVectorizer(sparse=True)
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)
    return X, dv

@task(retries=1, retry_delay_seconds=5)
def train_model(X_train, y_train, X_val, y_val, dv):
    with mlflow.start_run() as run:

        lr = LinearRegression()
        model = lr.fit(X_train, y_train)
        y_pred = lr.predict(X_val)

        rmse = root_mean_squared_error(y_val, y_pred)
        intercept = model.intercept_
        
        print("Intercept:", intercept)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_param("intercept", intercept)

        with open("models/preprocessor.b", "wb") as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")
        mlflow.sklearn.log_model(model, artifact_path="models_mlflow")
        return run.info.run_id

@task(retries=2, retry_delay_seconds=5)
def register_model(run_id):
    model_uri = f"runs:/{run_id}/model"
    model_name = "nyc-taxi-model"

    mlflow.register_model(model_uri=model_uri, name=model_name)

@flow
def run(year, month):
    df_train = read_dataframe(year=year, month=month)
    print(f"Result of data preparation row length = {len(df_train)}")
    
    next_year = year if month < 12 else year + 1
    next_month = month + 1 if month < 12 else 1
    df_val = read_dataframe(year=next_year, month=next_month)

    X_train, dv = create_X(df_train)
    X_val, _ = create_X(df_val, dv)

    target = 'duration'
    y_train = df_train[target].values
    y_val = df_val[target].values

    run_id = train_model(X_train, y_train, X_val, y_val, dv)
    print(f"MLflow run_id: {run_id}")
    
    register_model(run_id)

if __name__ == "__main__":
    run(2023, 3)
