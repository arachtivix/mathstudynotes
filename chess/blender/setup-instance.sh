#!/bin/bash

set -ex

echo "Setting up Blender instance..."
sudo yum update
sudo yum install git -y
sudo mkdr -p /var/wernerware/

cd /var/wernerware/
git clone https://github.com/arachtivix/mathstudynotes
cd mathstudynotes/chess/blender

echo "Installing Blender..."
sudo sh install-blender.sh

echo "Syncing assets from S3 bucket"
sudo mkdir -p assets
aws s3 sync s3://wernerware-blender-assets ./assets/
echo cd /var/wernerware/mathstudynotes/chess/blender >> ~/.bashrc