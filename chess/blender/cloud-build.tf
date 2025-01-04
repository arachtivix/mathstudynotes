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
