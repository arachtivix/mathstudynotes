# Space-optimized development container for mathstudynotes
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Create vscode user early
RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid vscode --shell /bin/bash --create-home vscode

# Install essential packages in a single optimized layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Basic development tools
    curl \
    wget \
    ca-certificates \
    git \
    unzip \
    sudo \
    # Build essentials (minimal)
    build-essential \
    # Java for Clojure development
    openjdk-17-jdk \
    # Node.js for ClojureScript
    nodejs \
    npm \
    # LaTeX (minimal install - space optimized)
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    # Clojure development helpers
    rlwrap \
    # Clean up everything in the same layer to minimize image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/* \
    && rm -rf /var/cache/apt/* \
    # Configure sudo for vscode user
    && usermod -aG sudo vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Reset environment
ENV DEBIAN_FRONTEND=

# Set working directory
WORKDIR /workspace

# Switch to vscode user by default
USER vscode

# Default command
CMD ["/bin/bash"]