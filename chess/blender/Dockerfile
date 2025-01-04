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