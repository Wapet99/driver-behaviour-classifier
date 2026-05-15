terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "driver-behaviour-classifier-tfstate"
    key = "dev"
    region = "ap-southeast-2"
  }
}

provider "aws" {
  region = var.aws_region
}

module "network" {
  source = "./modules/network"

  project_name = var.project_name
  vpc_cidr     = var.vpc_cidr
}

module "ecr" {
  source = "./modules/ecr"

  project_name = var.project_name
}

module "iam" {
  source = "./modules/iam"

  project_name      = var.project_name
  s3_model_bucket   = var.s3_model_bucket
  s3_model_key      = var.s3_model_key
}

module "alb" {
  source = "./modules/alb"

  project_name        = var.project_name
  vpc_id              = module.network.vpc_id
  public_subnet_ids   = module.network.public_subnet_ids
  target_port         = var.backend_container_port
}

module "ecs" {
  source = "./modules/ecs"

  project_name              = var.project_name
  vpc_id                    = module.network.vpc_id
  private_subnet_ids        = module.network.private_subnet_ids
  container_image           = var.container_image
  container_port            = var.backend_container_port
  desired_count             = var.ecs_desired_count
  task_execution_role_arn   = module.iam.task_execution_role_arn
  task_role_arn             = module.iam.task_role_arn
  alb_target_group_arn      = module.alb.target_group_arn
  alb_security_group_id     = module.alb.alb_security_group_id
  #log_group_name            = module.cloudwatch.log_group_name
  log_group_name            = "/${var.project_name}/backend"
  environment               = var.environment
  s3_model_bucket           = var.s3_model_bucket
  s3_model_key              = var.s3_model_key
  aws_region                = var.aws_region
}

module "cloudwatch" {
  source = "./modules/cloudwatch"

  project_name        = var.project_name
  alb_arn             = module.alb.alb_arn
  #ecs_cluster_name    = module.ecs.cluster_name
  #ecs_service_name    = module.ecs.service_name
}
