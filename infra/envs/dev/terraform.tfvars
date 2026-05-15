project_name          = "driver-behaviour-dev"
aws_region            = "ap-southeast-2"
environment           = "dev/"
container_image       = "536461878876.dkr.ecr.ap-southeast-2.amazonaws.com/driver-behaviour-dev-backend:latest"
ecs_desired_count     = 1
s3_model_bucket       = "driver-behaviour-classifier"
s3_model_key          = "models/minicnn_int8.onnx"
backend_container_port = 8000