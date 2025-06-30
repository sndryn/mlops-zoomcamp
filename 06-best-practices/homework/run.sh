export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
export S3_ENDPOINT_URL="http://127.0.0.1:4566"  

pipenv run pytest tests/

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    echo "error pytest"
fi

pipenv run python3 integration_test.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    echo "error integration test"
fi
