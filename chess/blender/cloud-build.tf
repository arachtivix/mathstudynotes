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


# Create security group for the EC2 instance
resource "aws_security_group" "blender_instance" {
  name        = "blender-instance-sg"
  description = "Security group for Blender G5 instance"

  # NFS for EFS
  ingress {
    from_port       = 2049
    to_port         = 2049
    protocol        = "tcp"
    security_groups = [aws_security_group.efs.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create security group for EFS
#resource "aws_security_group" "efs" {
#  name        = "blender-efs-sg"
#  description = "Security group for Blender EFS mount"

#  ingress {
#    from_port       = 2049
#    to_port         = 2049
#    protocol        = "tcp"
#    security_groups = [aws_security_group.blender_instance.id]
#  }
#}

# Create EFS mount target
resource "aws_efs_mount_target" "blender_workspace" {
  file_system_id  = aws_efs_file_system.blender_workspace.id
  subnet_id       = aws_subnet.private[0].id
  security_groups = [aws_security_group.efs.id]
}

# EC2 instance
resource "aws_instance" "blender_instance" {
  ami           = var.ami_id
  instance_type = "g5.xlarge"

  subnet_id                   = aws_subnet.private[0].id
  vpc_security_group_ids      = [aws_security_group.blender_instance.id]
  iam_instance_profile        = aws_iam_instance_profile.blender_instance.name
  associate_public_ip_address = false  # Can be private since we're using SSM

  root_block_device {
    volume_size = 10
    volume_type = "gp3"
  }

  user_data = base64encode(<<-EOF
              #!/bin/bash
              # Install AWS EFS utilities and SSM agent
              yum install -y amazon-efs-utils
              yum install -y https://s3.amazonaws.com/ec2-downloads-windows/SSMAgent/latest/linux_amd64/amazon-ssm-agent.rpm
              systemctl enable amazon-ssm-agent
              systemctl start amazon-ssm-agent

              # Create mount directory
              mkdir -p /workspace

              # Add EFS mount to fstab
              echo "${aws_efs_file_system.blender_workspace.id}:/ /workspace efs _netdev,tls,iam 0 0" >> /etc/fstab

              # Mount EFS
              mount -a
              EOF
  )
}

# Modify the EC2 IAM role to allow Systems Manager
resource "aws_iam_role_policy_attachment" "ssm_policy" {
  role       = aws_iam_role.blender_instance.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# Create instance profile
resource "aws_iam_instance_profile" "blender_instance" {
  name = "blender-instance-profile"
  role = aws_iam_role.blender_instance.name
}

# Create VPC
resource "aws_vpc" "blender_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "blender-vpc"
  }
}

# Create public subnets
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.blender_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "blender-public-${count.index + 1}"
  }
}

# Create private subnets
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.blender_vpc.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "blender-private-${count.index + 1}"
  }
}

# Create Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.blender_vpc.id

  tags = {
    Name = "blender-igw"
  }
}

# Create NAT Gateway
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "blender-nat"
  }

  depends_on = [aws_internet_gateway.main]
}

# Create route table for public subnets
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.blender_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "blender-public-rt"
  }
}

# Create route table for private subnets
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.blender_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name = "blender-private-rt"
  }
}

# Associate public subnets with public route table
resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# Associate private subnets with private route table
resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
}

# Outputs
output "vpc_id" {
  value = aws_vpc.blender_vpc.id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

# Add default security group with no ingress and egress allowed
resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.blender_vpc.id

  tags = {
    Name = "blender-default-sg"
  }
}

# Add VPC Flow Logs
resource "aws_flow_log" "vpc_flow_log" {
  iam_role_arn    = aws_iam_role.vpc_flow_log.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.blender_vpc.id
}

# CloudWatch Log Group for VPC Flow Logs
resource "aws_cloudwatch_log_group" "vpc_flow_log" {
  name              = "/aws/vpc/blender-vpc-flow-logs"
  retention_in_days = 30
}

# IAM role for VPC Flow Logs
resource "aws_iam_role" "vpc_flow_log" {
  name = "blender-vpc-flow-log-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "vpc-flow-logs.amazonaws.com"
        }
      }
    ]
  })
}

# IAM policy for VPC Flow Logs
resource "aws_iam_role_policy" "vpc_flow_log" {
  name = "blender-vpc-flow-log-policy"
  role = aws_iam_role.vpc_flow_log.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams"
        ]
        Effect = "Allow"
        Resource = "*"
      }
    ]
  })
}

