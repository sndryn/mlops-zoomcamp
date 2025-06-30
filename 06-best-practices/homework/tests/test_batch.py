from datetime import datetime

import pandas as pd

from batch import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
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
    df = pd.DataFrame(data, columns=columns)

    expected_value = pd.DataFrame(
        [
            ("-1", "-1", dt(1, 1), dt(1, 10), 9.0),
            ("1", "1", dt(1, 2), dt(1, 10), 8.0),
        ],
        columns=columns + ["duration"],
    )

    print(expected_value)
    categorical = ["PULocationID", "DOLocationID"]

    actual_value = prepare_data(df, categorical)

    pd.testing.assert_frame_equal(expected_value, actual_value)
