# -----------------------------
# Task Execution Role
# -----------------------------
data "aws_iam_policy_document" "task_execution_assume" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name               = "${var.project_name}-task-execution-role"
  assume_role_policy = data.aws_iam_policy_document.task_execution_assume.json
}

resource "aws_iam_role_policy_attachment" "task_execution_policy" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# -----------------------------
# Task Role (S3 model access)
# -----------------------------
data "aws_iam_policy_document" "task_assume" {
  statement {
    effect = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "task_policy" {
  statement {
    effect = "Allow"
    actions = ["s3:GetObject"]

    resources = [
      format("arn:aws:s3:::%s/%s", var.s3_model_bucket, var.s3_model_key)
    ]
  }
}

resource "aws_iam_role" "task" {
  name               = "${var.project_name}-task-role"
  assume_role_policy = data.aws_iam_policy_document.task_assume.json
}

resource "aws_iam_role_policy" "task_inline" {
  name   = "${var.project_name}-task-policy"
  role   = aws_iam_role.task.id
  policy = data.aws_iam_policy_document.task_policy.json
}
