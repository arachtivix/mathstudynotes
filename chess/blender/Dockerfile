FROM public.ecr.aws/docker/library/debian:stable-slim

# Install dependencies and download Blender in a single layer to minimize space
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /opt/blender \
    && cd /opt/blender \
    && wget -q https://download.blender.org/release/Blender3.4/blender-3.4.1-linux-x64.tar.xz \
    && tar -xf blender-3.4.1-linux-x64.tar.xz \
    && mv blender-3.4.1-linux-x64/* . \
    && rm -rf blender-3.4.1-linux-x64.tar.xz blender-3.4.1-linux-x64 \
    && apt-get purge -y wget \
    && apt-get autoremove -y \
    && rm -rf /tmp/* /var/tmp/*

# Add Blender to PATH
ENV PATH="/opt/blender:$PATH"

# Set the working directory
WORKDIR /workspace

# Command to run when container starts
ENTRYPOINT ["blender"]