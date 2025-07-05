variable "aws_region" {
    description = "AWS region to create resources"
    default     = "ap-southeast-1"
}

variable "project_id" {
    description = "project id"
    default     = "mlops-zoomcamp"
}

variable "source_stream_name" {
    description = "Name of source stream"
}

variable "output_stream_name" {
    description = "Name of output stream"
}

variable "model_bucket_name" {
    description = "S3 bucket"
}

variable "ecr_repo_name" {
    description = "ECR repo name"
}

variable "lambda_function_local_path" {
    description = "Local path of python lamda function file"
}

variable "docker_image_local_path" {
    description = "Local path of Dockerfile"
} 

variable "lambda_function_name" {
    description = "Name of lambda function"
  
}