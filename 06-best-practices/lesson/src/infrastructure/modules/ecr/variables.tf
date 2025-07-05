variable "ecr_repo_name" {
    description = "ecr repo name"
}

variable "ecr_image_tag" {
    type        = string
    description = "ECR image tag"
    default     = "latest"
}

variable "lambda_function_local_path" {
    type        = string
    description = "Local path to lambda function/ python file"
}

variable "docker_image_local_path" {
    type        = string
    description = "Local path to Dockerfile"
}

variable "region" {
    type        = string
    description = "region"
    default     = "ap-southeast-1"
}

variable "account_id" {

}