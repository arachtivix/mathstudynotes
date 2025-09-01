#!/bin/bash
set -e

echo "🩲⚡ Setting up Electric Underpants Clojure development environment..."

# Install Clojure CLI
echo "Installing Clojure CLI..."
curl -L https://github.com/clojure/brew-install/releases/latest/download/linux-install.sh | bash

# Verify installation
echo "Verifying Clojure installation..."
clojure --version

# Install clj-kondo for linting (used by the repository)
echo "Installing clj-kondo..."
curl -sLO https://raw.githubusercontent.com/clj-kondo/clj-kondo/master/script/install-clj-kondo
chmod +x install-clj-kondo
./install-clj-kondo --dir /usr/local/bin
rm install-clj-kondo

# Verify clj-kondo installation
echo "Verifying clj-kondo installation..."
clj-kondo --version

# Install Leiningen for projects using project.clj
echo "Installing Leiningen..."
curl -O https://raw.githubusercontent.com/technomancy/leiningen/stable/bin/lein
chmod a+x lein
sudo mv lein /usr/local/bin/
lein --version

echo "✅ Electric Underpants dev environment setup complete!"
echo "Available tools:"
echo "  - Clojure CLI: $(clojure --version)"
echo "  - clj-kondo: $(clj-kondo --version)"
echo "  - Leiningen: $(lein --version)"