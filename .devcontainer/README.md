# Electric Underpants Dev Container 🩲⚡

This devcontainer provides a complete development environment for the mathstudynotes repository, nicknamed "electric-underpants" for its electrifying development experience!

## What's Included

### Languages & Runtimes
- **Java 17** - For Clojure JVM support
- **Node.js 18** - For ClojureScript development
- **Clojure CLI** - Latest version for deps.edn projects
- **Leiningen** - For project.clj based projects

### Development Tools
- **clj-kondo** - Clojure linter (matches the CI configuration)
- **LaTeX** - For mathematical document processing
- **Common utilities** - With zsh, oh-my-zsh for better terminal experience

### VS Code Extensions
- **Calva** - Rich Clojure/ClojureScript development environment
- **LaTeX Workshop** - Full LaTeX editing and compilation support
- **Markdown linting** - For documentation quality
- **YAML/JSON support** - For configuration files

### Pre-configured Ports
- **3000** - Common development server port
- **8080** - Alternative web server port  
- **9500** - REPL or other Clojure tooling

## Prebuild Support

This devcontainer is configured for GitHub Codespaces prebuilds, which means:
- Faster startup times when creating new Codespaces
- All dependencies are pre-installed and cached
- Ready to start coding immediately

## Usage

### In GitHub Codespaces
1. Open the repository in Codespaces
2. The prebuild will provide a fully configured environment
3. Start coding in Clojure, LaTeX, or any other language in the repo

### Locally with VS Code
1. Install the Dev Containers extension
2. Open the repository in VS Code
3. Use "Reopen in Container" command
4. Wait for the initial setup to complete

## Directory Structure Support

This environment supports all the various project types in the repository:
- Clojure projects with `deps.edn` 
- Clojure projects with `project.clj`
- ClojureScript projects
- LaTeX documents
- General development workflows

Welcome to the Electric Underpants! ⚡