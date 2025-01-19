#!/bin/bash

set -ex

# Update system and install dependencies
sudo yum update -y
sudo yum install -y libXi libXrender libXfixes libXcomposite mesa-libGL mesa-libGLU \
    libXrandr libXinerama libXcursor zlib libstdc++ freetype fontconfig \
    libXext libX11 libXxf86vm libxkbcommon-x11

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
