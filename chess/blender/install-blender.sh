#!/bin/bash

# Update system and install dependencies
sudo yum update -y
sudo yum install -y libXi libXrender libXfixes libXcomposite mesa-libGL mesa-libGLU \
    libXrandr libXinerama libXcursor zlib libstdc++ freetype fontconfig \
    libXext libX11 libXxf86vm

# Create directory for Blender
sudo mkdir -p /opt/blender
cd /opt/blender

# Download Blender 3.4.1
wget https://download.blender.org/release/Blender3.4/blender-3.4.1-linux-x64.tar.xz

# Extract Blender
sudo tar -xf blender-3.4.1-linux-x64.tar.xz
sudo mv blender-3.4.1-linux-x64/* .
sudo rm -r blender-3.4.1-linux-x64
sudo rm blender-3.4.1-linux-x64.tar.xz

# Create symbolic link to make Blender accessible system-wide
sudo ln -s /opt/blender/blender /usr/local/bin/blender

# Set permissions
sudo chown -R root:root /opt/blender
sudo chmod 755 /opt/blender/blender

# Verify installation
blender --version

# Optional: Install Python dependencies if needed for rendering
sudo yum install -y python3-pip
pip3 install numpy

# Create a test to ensure Blender can run in headless mode
echo "import bpy; print('Blender Python API works!')" > /tmp/test.py
blender --background --python /tmp/test.py
