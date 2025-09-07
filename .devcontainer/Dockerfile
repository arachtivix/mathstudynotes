# Multi-stage build for space optimization
FROM ubuntu:22.04 as base

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Create vscode user early
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid vscode --shell /bin/bash --create-home vscode

# Install essential packages in a single layer with cleanup
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Basic tools
    curl \
    wget \
    ca-certificates \
    git \
    unzip \
    sudo \
    # Build tools (minimal)
    build-essential \
    # Java for Clojure (OpenJDK 17)
    openjdk-17-jdk \
    # Node.js for ClojureScript  
    nodejs \
    npm \
    # LaTeX (minimal install)
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    # Clojure development tools
    rlwrap \
    # Clean up in same layer to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/* \
    # Add vscode user to sudo group
    && usermod -aG sudo vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Copy and run setup script for Clojure tools
COPY setup-clojure.sh /tmp/setup-clojure.sh
RUN chmod +x /tmp/setup-clojure.sh && /tmp/setup-clojure.sh && rm /tmp/setup-clojure.sh

# Final stage - clean minimal image
FROM base as final

# Reset environment
ENV DEBIAN_FRONTEND=

# Set working directory
WORKDIR /workspace

# Switch to vscode user by default
USER vscode

# Default command
CMD ["/bin/bash"]