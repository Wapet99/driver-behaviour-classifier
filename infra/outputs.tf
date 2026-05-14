output "alb_dns_name" {
  value       = module.alb.alb_dns_name
  description = "Public DNS name of the ALB"
}

output "ecs_cluster_name" {
  value       = module.ecs.cluster_name
  description = "ECS cluster name"
}

output "ecs_service_name" {
  value       = module.ecs.service_name
  description = "ECS service name"
}
