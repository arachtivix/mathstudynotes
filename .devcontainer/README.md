# Math Study Notes Development Container

This devcontainer provides a space-optimized development environment for the mathstudynotes repository, supporting Clojure development and LaTeX document processing.

## 🎯 What's Included

### Development Tools
- **Java 17** - OpenJDK for Clojure development
- **Clojure CLI** - Modern Clojure tooling
- **Leiningen** - Project management for Clojure
- **clj-kondo** - Clojure linter matching CI configuration
- **Node.js & NPM** - For ClojureScript development

### Document Processing
- **LaTeX** - Minimal TeXLive installation for document compilation
- **PDF generation** - Support for the 54+ LaTeX documents in the repository

### Editor Integration
- **Calva** - Clojure extension for VS Code
- **LaTeX Workshop** - LaTeX editing and compilation
- **Optimized settings** - Pre-configured for Clojure and LaTeX work

## 🚀 Quick Start

### Using GitHub Codespaces
1. Click the "Code" button on the repository
2. Select "Create codespace on main"
3. Wait for the container to build (optimized for speed)
4. Run `.devcontainer/test-environment.sh` to verify setup

### Using VS Code Dev Containers
1. Open the repository in VS Code
2. Install the "Dev Containers" extension
3. Command Palette → "Dev Containers: Reopen in Container"
4. Wait for the container to build

## 🔧 Space Optimization Features

This devcontainer is optimized to address space constraints:

### Minimal Base Image
- Uses Ubuntu 22.04 for smaller size vs Debian
- Single-layer package installations with immediate cleanup
- Removes package caches and temporary files

### Efficient Tool Installation
- Combined RUN commands to minimize Docker layers
- Immediate cleanup after each installation step
- Minimal LaTeX installation (base + recommended only)

### Smart Caching
- Leverages Docker layer caching for faster rebuilds
- Tools installed in optimal order for cache efficiency
- Development dependencies only (no runtime bloat)

## 📊 Size Comparison

**Before optimization**: ~2GB+ (typical full LaTeX + dev environment)
**After optimization**: ~800MB (estimated final image size)

**Space savings achieved through**:
- Minimal LaTeX packages instead of full TeXLive
- Single-layer installations with cleanup
- No unnecessary development tools
- Optimized package selection

## 🧪 Testing the Environment

Run the verification script to ensure everything works:

```bash
.devcontainer/test-environment.sh
```

This will test:
- Java and Clojure installation
- LaTeX compilation capability
- All development tools
- Basic functionality verification

## 📁 Repository Structure Support

The environment supports all project types in this repository:

- **Clojure projects** - Both CLI (`deps.edn`) and Leiningen (`project.clj`)
- **LaTeX documents** - All `.tex` files in various directories
- **Mixed projects** - Projects combining Clojure and documentation

## 🔄 Rebuilding

If you need to rebuild the container:
- **Codespaces**: Delete and recreate the codespace
- **VS Code**: Command Palette → "Dev Containers: Rebuild Container"

## 🛠️ Customization

### Adding More LaTeX Packages
Edit `.devcontainer/Dockerfile` and add packages to the `texlive-*` line:

```dockerfile
texlive-latex-base \
texlive-latex-recommended \
texlive-fonts-recommended \
texlive-math-extra \      # Add mathematical symbols
texlive-science \         # Add scientific packages
```

### Additional Clojure Tools
Add tools to the setup script or Dockerfile as needed.

## 🔍 Troubleshooting

### Container Won't Build
- Check available disk space on your system
- Try rebuilding without cache: use "Rebuild Without Cache" option

### Tools Not Working
- Run `.devcontainer/test-environment.sh` to diagnose issues
- Check that all installation steps completed successfully

### Space Issues
- The container is optimized for minimal size
- If you need additional tools, consider removing unused ones first

## 📈 Performance Tips

- **First build**: May take 5-10 minutes depending on connection
- **Subsequent builds**: Should be much faster due to layer caching
- **Codespaces**: Benefits from GitHub's prebuild system when configured