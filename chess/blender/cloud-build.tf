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
  name = "wernerware-blender-ec2-profile"
  role = aws_iam_role.ec2_ssm_role.name
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

# EC2 Instance
resource "aws_instance" "blender_instance" {
  ami           = "ami-031290e21cc458792"
  instance_type = "g6.48xlarge"

  subnet_id                   = "subnet-0cd3d3cf47168c732"
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_ssm_profile.name

  root_block_device {
    volume_size = 45  # Size in GB
    volume_type = "gp3"
  }

  tags = {
    Name = "wernerware-blender-instance"
  }

  # Make sure SSM agent is installed
  user_data = <<-EOF
              #!/bin/bash
              systemctl enable amazon-ssm-agent
              systemctl start amazon-ssm-agent
              EOF
}

output "blender_instance_id" {
  description = "The ID of the Blender EC2 instance"
  value       = aws_instance.blender_instance.id
}

# Create the S3 bucket
resource "aws_s3_bucket" "blender_assets" {
  bucket = "wernerware-blender-assets"
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
