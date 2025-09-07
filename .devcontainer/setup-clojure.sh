#!/bin/bash

# Clojure Development Environment Setup Script
# This script is optimized for space and speed with fallback mechanisms

set -e

echo "🚀 Setting up Clojure development environment..."

# Function to download with fallback
download_file() {
    local url="$1"
    local output="$2"
    echo "📥 Downloading $output from $url"
    
    # Try secure first, then insecure as fallback
    if ! curl -L --connect-timeout 30 --max-time 120 -o "$output" "$url"; then
        echo "⚠️  Secure download failed, trying insecure fallback..."
        curl -L --insecure --connect-timeout 30 --max-time 120 -o "$output" "$url"
    fi
}

# Install Clojure CLI
echo "☕ Installing Clojure CLI..."
cd /tmp
download_file "https://github.com/clojure/brew-install/releases/latest/download/linux-install.sh" "linux-install.sh"
chmod +x linux-install.sh
./linux-install.sh
rm linux-install.sh

# Install Leiningen
echo "🎯 Installing Leiningen..."
download_file "https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein" "/usr/local/bin/lein"
chmod +x /usr/local/bin/lein

# Install clj-kondo with fallback to direct binary download
echo "🔍 Installing clj-kondo..."
if ! download_file "https://raw.githubusercontent.com/clj-kondo/clj-kondo/master/script/install-clj-kondo" "install-clj-kondo"; then
    echo "📦 Fallback: Installing clj-kondo binary directly..."
    # Fallback to direct binary download
    download_file "https://github.com/clj-kondo/clj-kondo/releases/latest/download/clj-kondo-linux-amd64.zip" "clj-kondo.zip"
    unzip clj-kondo.zip
    mv clj-kondo /usr/local/bin/
    chmod +x /usr/local/bin/clj-kondo
    rm clj-kondo.zip
else
    chmod +x install-clj-kondo
    ./install-clj-kondo
    rm install-clj-kondo
fi

# Clean up
rm -rf /tmp/*

echo "✅ Clojure development environment setup complete!"
echo "📋 Installed tools:"
java -version 2>&1 | head -1 && echo ""
clojure --version
echo "Node.js: $(node --version)"
echo "NPM: $(npm --version)"
echo "clj-kondo: $(clj-kondo --version)"

echo "🎉 All tools installed and verified!"