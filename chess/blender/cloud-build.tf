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

# Create EFS file system for persistent workspace
resource "aws_efs_file_system" "blender_workspace" {
  creation_token = "blender-workspace"
  encrypted      = true

  tags = {
    Name = "BlenderWorkspace"
  }
}
