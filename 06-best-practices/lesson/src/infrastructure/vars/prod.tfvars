source_stream_name  = "prod_ride_events"
output_stream_name  = "prod_ride_predictions"
model_bucket_name   = "prod-mlflow-model"
ecr_repo_name               = "prod_stream_model_duration"
lambda_function_local_path  = "../lambda_function.py"
lambda_function_name        = "prod_prediction_lambda"
docker_image_local_path     = "../Dockerfile"

