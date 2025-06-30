import os
from datetime import datetime

import pandas as pd

from batch import read_data, save_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def prepare_input_data(year, month):
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]

    columns = [
        "PULocationID",
        "DOLocationID",
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
    ]
    df_input = pd.DataFrame(data, columns=columns)

    input_pattern = os.getenv("INPUT_FILE_PATTERN")
    input_file = input_pattern.format(year=year, month=month)

    save_data(df_input, input_file)

    # checking in cli: aws s3 ls s3://nyc-duration/in/ --endpoint-url=http://localhost:4566


year, month = 2023, 1
prepare_input_data(year, month)

# run batch.py
os.system("python3 batch.py 2023 1")

df_result = read_data(os.getenv("OUTPUT_FILE_PATTERN").format(year=year, month=month))
print("Sum of predicted duration", df_result["predicted_duration"].sum())
