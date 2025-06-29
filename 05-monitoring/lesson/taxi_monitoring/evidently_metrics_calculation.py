import datetime
import time
import random
import logging
import pytz
import pandas as pd
import psycopg
import joblib
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

tz = pytz.timezone("Asia/Jakarta")

create_table_statement = """
drop table if exists metrics;
create table metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns int,
	share_missing_val float
)
"""

num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
cat_features = ["PULocationID", "DOLocationID"]

reference_data = pd.read_parquet("data/reference.parquet")
with open("models/lin_reg.bin", "rb") as f_in:
    model = joblib.load(f_in)

raw_data = pd.read_parquet("data/green_tripdata_2022-02.parquet")

begin = datetime.datetime(2022, 2, 1, 0, 0)

column_mapping = ColumnMapping(
    target=None,
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features
)

report = Report(metrics=[
    ColumnDriftMetric(column_name='prediction'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric(),
])

def prep_db():
    with psycopg.connect("host=localhost port=5432 user=postgres password=example123!", autocommit=True) as conn:
        res = conn.execute("SELECT 1 FROM pg_database WHERE datname='taxi_monitoring'")
        if len(res.fetchall()) == 0:
            conn.execute("create database taxi_monitoring;")

    with psycopg.connect("host=localhost port=5432 user=postgres password=example123! dbname=taxi_monitoring", autocommit=True) as conn:
        conn.execute(create_table_statement)

def calculate_metrics_postgresql(curr, i):
    current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
		(raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]

    current_data.fillna(0, inplace=True)
    current_data["prediction"] = model.predict(current_data[num_features + cat_features])

    report.run(reference_data=reference_data,
                current_data=current_data,
                column_mapping=column_mapping)

    result = report.as_dict()
    prediction_drift = result["metrics"][0]["result"]["drift_score"]
    num_drifted_columns = result["metrics"][1]["result"]["number_of_drifted_columns"]
    share_missing_values = result["metrics"][2]["result"]["current"]["share_of_missing_values"]

    curr.execute(
        "insert into metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_val) values (%s, %s, %s, %s)",
        (begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values)
    )

def main():
    prep_db()
    last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
    with psycopg.connect("host=localhost port=5432 user=postgres password=example123! dbname=taxi_monitoring", autocommit=True) as conn:
        for i in range(0, 27):
            with conn.cursor() as curr:
                calculate_metrics_postgresql(curr, i)

                new_send = datetime.datetime.now()
                seconds_elapsed = (new_send - last_send).total_seconds()
                if seconds_elapsed < SEND_TIMEOUT:
                    time.sleep(SEND_TIMEOUT - seconds_elapsed)
                while last_send < new_send:
                    last_send = last_send + datetime.timedelta(seconds=10)
                logging.info("data sent")

main()