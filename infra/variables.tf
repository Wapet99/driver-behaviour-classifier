variable "project_name" {
  type        = string
  description = "Project name prefix for resources"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
}

variable "environment" {
  type        = string
  description = "Environment name (dev, prod)"
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

variable "backend_container_port" {
  type        = number
  description = "Port exposed by FastAPI container"
  default     = 8000
}

variable "container_image" {
  type        = string
  description = "ECR image URI for backend"
}

variable "ecs_desired_count" {
  type        = number
  description = "Desired ECS task count"
  default     = 1
}

variable "s3_model_bucket" {
  type        = string
  description = "S3 bucket for ONNX model"
}

variable "s3_model_key" {
  type        = string
  description = "S3 key for ONNX model"
}
