
## Module Responsibilities
### modules/network
- VPC
- Public + private subnets
- NAT gateway
- Route tables
- Security groups

Development impact:
- No longer networking manually
- ECS tasks run in private subnets (best practice)
- ALB sits in public subnets

### modules/ecr
- ECR repository
- Lifecycle policy (keep last N images)

Devlopment impact:
- Push docker images here before deployment
- CI/CD pipeline would use this repo

### module/iam
- ECS task execution role
- ECS task role with S3 read permissions
- CloudWatch logging permissions

Development impact:
- Backend doesn't need AWS keys
- S3 model loading becomes secure and automatic

### modules/alb
- ALB
- Listener (port 80 or 443)
- Target group
- Health checks (`/health`)

Development impact:
- Automatic health-based restarts
- ALB latency + 5xx metrics for free

### modules/ecs
- ECS cluster
- Task definition
- Fargate service
- Autoscaling policies

Development impact:
- Deployments become one command: `terraform apply`
- ECS pulls image from ECR
- ECS injects env vars
- ECS sends logs to CloudWatch

### modules/cloudwatch
- Log group
- Dashboard
- Alarms:
    - ALB 5xx
    - ALB latency
    - ECS CPU/memory
    - Custom metrics (inference latency)

Development impact:
- Can see model's performance
- Get alerts when inference slows or fails

## Deployment
From project root:
```bash
cd infra
terraform init
terraform apply
```
Terraform will:
- Create/update ECS service
- Trigger a new deployment
- Update ALB routing
- Update CloudWatch alarms

## Decisions
### Modular Terraform
- Make infra readable
- Support component reuse
- Support deploy dev/prod with different settings
- Proper IaC structure

### ECS Fargate over EC2
Fargate gives:
- No servers to manage
- Faster deployments
- Built-in autoscaling
- Cleaner IAM boundaries
- Solid fit for containerised inference

### ALB instead of Nginx
In AWS:
- ALB handles routing, health checks, scaling
- ALB integrates with ECS natively
- ALB gives metrics (latency, server errors) for free
Nginx not needed unless need custom caching or rewrites.

### CloudWatch Logs + Metrics
FastAPI backend already logs JSON
Terraform can:
- Create a log group
- Attach it to the ECS task
- Create dashboards
- Create alarms
Crucial observability layer for production.