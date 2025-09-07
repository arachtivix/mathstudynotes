#!/bin/bash

# Clojure Development Environment Setup Script
# This script runs as a post-create command with proper network access
# Optimized for space and speed

set -e

echo "🚀 Setting up Clojure development environment..."

# Check if already installed to avoid reinstalling
if command -v clojure >/dev/null 2>&1 && command -v lein >/dev/null 2>&1 && command -v clj-kondo >/dev/null 2>&1; then
    echo "✅ Clojure tools already installed, skipping setup"
    exit 0
fi

# Install Clojure CLI
if ! command -v clojure >/dev/null 2>&1; then
    echo "☕ Installing Clojure CLI..."
    cd /tmp
    curl -L -O https://github.com/clojure/brew-install/releases/latest/download/linux-install.sh
    chmod +x linux-install.sh
    sudo ./linux-install.sh
    rm linux-install.sh
fi

# Install Leiningen
if ! command -v lein >/dev/null 2>&1; then
    echo "🎯 Installing Leiningen..."
    curl -L -o /tmp/lein https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
    sudo mv /tmp/lein /usr/local/bin/lein
    sudo chmod +x /usr/local/bin/lein
    # Pre-install Leiningen dependencies to avoid first-run delay
    lein version
fi

# Install clj-kondo
if ! command -v clj-kondo >/dev/null 2>&1; then
    echo "🔍 Installing clj-kondo..."
    cd /tmp
    curl -sLO https://raw.githubusercontent.com/clj-kondo/clj-kondo/master/script/install-clj-kondo
    chmod +x install-clj-kondo
    sudo ./install-clj-kondo
    rm install-clj-kondo
fi

# Clean up
rm -rf /tmp/*

echo "✅ Clojure development environment setup complete!"
echo "📋 Installed tools:"
echo "   - Java: $(java -version 2>&1 | head -1)"
echo "   - Clojure CLI: $(clojure --version 2>/dev/null || echo 'Error getting version')"
echo "   - Leiningen: $(lein version 2>/dev/null | head -1 || echo 'Error getting version')"
echo "   - Node.js: $(node --version)"
echo "   - NPM: $(npm --version)"
echo "   - clj-kondo: $(clj-kondo --version 2>/dev/null || echo 'Error getting version')"

echo "🎉 All tools installed!"