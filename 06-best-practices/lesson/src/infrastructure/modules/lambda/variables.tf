variable "output_stream_name" {
    description = "Name of the output stream where all the events will be passed"
}

variable "output_stream_arn" {
    description = "ARN of output stream where all the events will be passed"
}

variable "source_stream_name" {
  type        = string
  description = "Name of input stream where all the events will be consumed"
}

variable "source_stream_arn" {
    description = "ARN of input stream where all the events will be consumed"
}

variable "model_bucket_name" {
    description = "Model bucket name"
}

variable "image_uri" {
    description = "Image URI"
}

variable "lambda_function_name" {
    description = "Name of the lambda function"
}
