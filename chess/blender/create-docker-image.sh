#!/usr/bin/bash
set -e

# Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPO_NAME="wernerware-blender"
IMAGE_TAG="latest"

echo "=== Creating ECR repository if it doesn't exist ==="
aws ecr create-repository \
    --repository-name ${ECR_REPO_NAME} \
    --image-scanning-configuration scanOnPush=true \
    || true

echo "=== Authenticating Docker with ECR ==="
aws ecr get-login-password --region ${AWS_REGION} | \
    docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

echo "=== Creating Dockerfile ==="
cat << 'EOF' > Dockerfile
FROM public.ecr.aws/docker/library/debian:stable-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    libxrender1 \
    libxi6 \
    libgl1 \
    libxkbcommon0 \
    libxcb-keysyms1 \
    libxcb-shape0 \
    libxcb-icccm4 \
    libxcb-render-util0 \
    libxcb-randr0 \
    libxcb-xfixes0 \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

# Create directory for Blender
WORKDIR /opt/blender

# Download and extract Blender 3.4.1
RUN wget https://download.blender.org/release/Blender3.4/blender-3.4.1-linux-x64.tar.xz \
    && tar -xf blender-3.4.1-linux-x64.tar.xz \
    && rm blender-3.4.1-linux-x64.tar.xz \
    && mv blender-3.4.1-linux-x64/* . \
    && rmdir blender-3.4.1-linux-x64

# Add Blender to PATH
ENV PATH="/opt/blender:$PATH"

# Set the working directory
WORKDIR /workspace

# Command to run when container starts
ENTRYPOINT ["blender"]
EOF

echo "=== Building Docker image ==="
docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} .

echo "=== Tagging Docker image ==="
docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}

echo "=== Pushing Docker image to ECR ==="
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}

echo "=== Cleanup ==="
rm Dockerfile

echo "=== Done! ==="
echo "Your image is now available at: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}"
