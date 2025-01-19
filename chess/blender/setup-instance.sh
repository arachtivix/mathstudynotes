#!/bin/bash

set -ex

echo "Setting up Blender instance..."
sudo yum update
sudo yum install git -y
sudo pip3 install boto3

sudo mkdir -p /var/wernerware/

cd /var/wernerware/
git clone https://github.com/arachtivix/mathstudynotes
cd mathstudynotes/chess/blender

echo "Installing Blender..."
sudo sh install-blender.sh

echo "Syncing assets from S3 bucket"
sudo mkdir -p assets
aws s3 sync s3://wernerware-blender-assets ./assets/
echo cd /var/wernerware/mathstudynotes/chess/blender >> ~/.bashrc

sudo python3 -m pip install boto3
sudo chmod +x blend-file-queue-listener.py

sudo cp ./blend-file-queue-listener.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable blend-file-queue-listener
sudo systemctl start blend-file-queue-listener

# Verify blender installation
blender --version

# Create a test to ensure Blender can run in headless mode
echo "import bpy; print('Blender Python API works!')" > /tmp/test.py
blender --background --python /tmp/test.py