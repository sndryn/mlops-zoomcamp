import pickle
import pandas as pd
import argparse


categorical = ['PULocationID', 'DOLocationID']

def load_model():
    with open('model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model

def predict(df):
    dv, model = load_model()

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    
    df_results = df[["ride_id"]]
    df_results["y_pred"] = y_pred

    return df_results


def read_data(year, month):
    filename = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df


def download_result(df, filename):
    df.to_parquet(
        filename,
        engine='pyarrow',
        compression=None,
        index=False
    )

def run(year, month):
    df = read_data(year, month)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    df_results = predict(df)

    filename = "output.parquet"
    download_result(df_results, filename)

    print(f"Mean of predicted duration for {year:04d}-{month:02d}:", df_results["y_pred"].mean())

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Train a model to predict taxi trip duration.')
    parser.add_argument('--year', type=int, required=True, help='Year of the data to train on')
    parser.add_argument('--month', type=int, required=True, help='Month of the data to train on')
    args = parser.parse_args()

    run_id = run(year=args.year, month=args.month)
