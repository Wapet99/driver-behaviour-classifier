# remove to prevent overlap with ecs
#resource "aws_cloudwatch_log_group" "app" {
#  name              = "/${var.project_name}/backend"
#  retention_in_days = 14
#}

# Example alarm skeleton – fill thresholds later
resource "aws_cloudwatch_metric_alarm" "alb_5xx" {
  alarm_name          = "${var.project_name}-alb-5xx"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "HTTPCode_ELB_5XX_Count"
  namespace           = "AWS/ApplicationELB"
  period              = 60
  statistic           = "Sum"
  threshold           = 1

  dimensions = {
    LoadBalancer = var.alb_arn
  }
}