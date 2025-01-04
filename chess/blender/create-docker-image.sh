#!/usr/bin/bash
set -ex

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
