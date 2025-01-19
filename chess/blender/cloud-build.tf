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

# Initialize the random provider
provider "random" {}

# Generate a random string
resource "random_string" "instance_profile_addon" {
  length  = 8
  special = false
  upper   = false
  lower   = true
  number  = true
}

# Create IAM role for EC2
resource "aws_iam_role" "ec2_ssm_role" {
  name = "wernerware-blender-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

# Attach AWS managed policy for SSM
resource "aws_iam_role_policy_attachment" "ssm_managed_instance_core" {
  role       = aws_iam_role.ec2_ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Create custom policy for additional Session Manager permissions
resource "aws_iam_role_policy" "ssm_custom" {
  name = "session-manager-custom"
  role = aws_iam_role.ec2_ssm_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:UpdateInstanceInformation",
          "ssmmessages:CreateControlChannel",
          "ssmmessages:CreateDataChannel",
          "ssmmessages:OpenControlChannel",
          "ssmmessages:OpenDataChannel"
        ]
        Resource = "*"
      }
    ]
  })
}

# Create the instance profile
resource "aws_iam_instance_profile" "ec2_ssm_profile" {
  name = "wernerware-blender-ec2-profile-${random_string.instance_profile_addon.result}"
  role = aws_iam_role.ec2_ssm_role.name
  lifecycle {
    create_before_destroy = true
  }
}

# Security Group for the EC2 instance
resource "aws_security_group" "ec2_sg" {
  name        = "wernerware-blender-sg"
  description = "Security group for Blender EC2 instance"
  vpc_id      = "vpc-0630cdab2116279f7"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "wernerware-blender-sg"
  }
}

data "template_file" "setup_script" {
  template = file("${path.module}/setup-instance.sh")
}

variable "ec2_ami" {
  type = string
  default = "ami-043a5a82b6cf98947"
}

variable "volume_size" {
  type = number
  default = 15
}

variable "instance_type" {
  type = string
  default = "t2.micro"
}

# EC2 Instance
resource "aws_instance" "blender_instance" {
  ami           = var.ec2_ami
  instance_type = var.instance_type

  subnet_id                   = "subnet-0cd3d3cf47168c732"
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_ssm_profile.name

  root_block_device {
    volume_size = var.volume_size
    volume_type = "gp3"
  }

  tags = {
    Name = "wernerware-blender-instance"
  }
  
  # Add the user_data configuration
  user_data = base64encode(data.template_file.setup_script.rendered)

}

output "blender_instance_id" {
  description = "The ID of the Blender EC2 instance"
  value       = aws_instance.blender_instance.id
}

# Create the S3 bucket
resource "aws_s3_bucket" "blender_assets" {
  bucket = "wernerware-blender-assets"
}

# Create the S3 bucket
resource "aws_s3_bucket" "blender_renders" {
  bucket = "wernerware-blender-renders"
}

# Block public access to the bucket
resource "aws_s3_bucket_public_access_block" "blender_assets" {
  bucket = aws_s3_bucket.blender_assets.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Add S3 permissions to the existing EC2 role
resource "aws_iam_role_policy" "s3_access" {
  name = "s3-blender-assets-access"
  role = aws_iam_role.ec2_ssm_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = [
          aws_s3_bucket.blender_assets.arn,
          "${aws_s3_bucket.blender_assets.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_ssm_document" "setup_blender" {
  name            = "setup-blender-environment"
  document_type   = "Command"
  document_format = "YAML"

  content = <<DOC
schemaVersion: '2.2'
description: 'Setup Blender environment by cloning repository and running setup script'
parameters: {}
mainSteps:
  - action: aws:runShellScript
    name: setupBlenderEnvironment
    inputs:
      runCommand:
        - sudo yum update
        - sudo yum install git -y
        - sudo mkdr -p /var/wernerware/
        - cd /var/wernerware
        - git clone https://github.com/arachtivix/mathstudynotes
        - cd mathstudynotes/chess/blender
        - sudo bash setup-instance.sh
DOC

  tags = {
    Name = "setup-blender-environment"
    Purpose = "Blender Environment Setup"
  }
}
