terraform {
  backend "s3" {
    bucket         = "wernerware-blender-terraform"
    key            = "terraform.tfstate"
    region         = "us-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Get reference to existing ECR repository
data "aws_ecr_repository" "blender" {
  name = "wernerware-blender"
}

# Output the repository URL for reference
output "repository_url" {
  value = data.aws_ecr_repository.blender.repository_url
}

# Output the registry ID
output "registry_id" {
  value = data.aws_ecr_repository.blender.registry_id
}

# Output the ARN
output "repository_arn" {
  value = data.aws_ecr_repository.blender.arn
}


# Create ECS task execution role
resource "aws_iam_role" "ecs_task_execution_role" {
  name = "blender-task-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Attach the AWS managed policy for ECS task execution
resource "aws_iam_role_policy_attachment" "ecs_task_execution_role_policy" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Create ECS task definition
resource "aws_ecs_task_definition" "blender_task" {
  family                   = "blender-task"
  requires_compatibilities = ["FARGATE"]
  network_mode            = "awsvpc"
  cpu                     = "2048"  # 2 vCPU
  memory                  = "4096"  # 4GB
  execution_role_arn      = aws_iam_role.ecs_task_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = "blender-container"
      image = "${data.aws_ecr_repository.blender.repository_url}:latest"
      
      essential = true
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/blender-task"
          "awslogs-region"        = "us-east-1"
          "awslogs-stream-prefix" = "ecs"
        }
      }

      mountPoints = [
        {
          sourceVolume  = "workspace"
          containerPath = "/workspace"
          readOnly     = false
        }
      ]

      environment = [
        {
          name  = "BLENDER_ARGS"
          value = "--background"  # Run Blender in background mode by default
        }
      ]
    }
  ])

  volume {
    name = "workspace"
    efs_volume_configuration {
      file_system_id = aws_efs_file_system.blender_workspace.id
      root_directory = "/"
    }
  }

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture       = "X86_64"
  }
}

# Create CloudWatch log group for container logs
resource "aws_cloudwatch_log_group" "blender_logs" {
  name              = "/ecs/blender-task"
  retention_in_days = 30
}

# Create EFS file system for persistent workspace
resource "aws_efs_file_system" "blender_workspace" {
  creation_token = "blender-workspace"
  encrypted      = true

  tags = {
    Name = "BlenderWorkspace"
  }
}

# Output the task definition ARN
output "task_definition_arn" {
  value = aws_ecs_task_definition.blender_task.arn
}

# Output the task definition family
output "task_definition_family" {
  value = aws_ecs_task_definition.blender_task.family
}

# Optional: Create a task role if your Blender container needs AWS permissions
resource "aws_iam_role" "blender_task_role" {
  name = "blender-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# Add task role to the task definition
resource "aws_ecs_task_definition" "blender_task" {
  # ... (previous configuration) ...
  task_role_arn = aws_iam_role.blender_task_role.arn
  # ... (rest of configuration) ...
}
