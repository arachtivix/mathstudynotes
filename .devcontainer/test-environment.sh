#!/bin/bash

# Environment Verification Script
# Tests that all development tools are working correctly

set -e

echo "🧪 Testing Math Study Notes Development Environment..."
echo "=================================================="

# Test Java
echo -n "☕ Java: "
if java -version 2>&1 | grep -q "openjdk version"; then
    echo "✅ $(java -version 2>&1 | head -1 | cut -d'"' -f2)"
else
    echo "❌ Java not found or not working"
    exit 1
fi

# Test Clojure CLI
echo -n "🎯 Clojure CLI: "
if command -v clojure >/dev/null 2>&1; then
    version=$(clojure --version 2>&1 | head -1)
    echo "✅ $version"
    
    # Test Clojure evaluation
    echo -n "   Testing Clojure evaluation: "
    result=$(echo '(+ 1 2 3)' | clojure -M -)
    if [[ "$result" == "6" ]]; then
        echo "✅ Expression evaluation works"
    else
        echo "❌ Expression evaluation failed"
        exit 1
    fi
else
    echo "❌ Clojure CLI not found"
    exit 1
fi

# Test Leiningen
echo -n "🚀 Leiningen: "
if command -v lein >/dev/null 2>&1; then
    version=$(lein version | head -1)
    echo "✅ $version"
else
    echo "❌ Leiningen not found"
    exit 1
fi

# Test clj-kondo
echo -n "🔍 clj-kondo: "
if command -v clj-kondo >/dev/null 2>&1; then
    version=$(clj-kondo --version)
    echo "✅ $version"
else
    echo "❌ clj-kondo not found"
    exit 1
fi

# Test Node.js
echo -n "🟢 Node.js: "
if command -v node >/dev/null 2>&1; then
    version=$(node --version)
    echo "✅ $version"
else
    echo "❌ Node.js not found"
    exit 1
fi

# Test NPM
echo -n "📦 NPM: "
if command -v npm >/dev/null 2>&1; then
    version=$(npm --version)
    echo "✅ v$version"
else
    echo "❌ NPM not found"
    exit 1
fi

# Test LaTeX
echo -n "📄 LaTeX: "
if command -v pdflatex >/dev/null 2>&1; then
    echo "✅ Available"
    
    # Test basic LaTeX compilation
    echo -n "   Testing LaTeX compilation: "
    cat > /tmp/test.tex << 'EOF'
\documentclass{article}
\begin{document}
Hello, LaTeX!
\end{document}
EOF
    
    if pdflatex -output-directory=/tmp -interaction=nonstopmode /tmp/test.tex >/dev/null 2>&1; then
        echo "✅ LaTeX compilation works"
        rm -f /tmp/test.*
    else
        echo "❌ LaTeX compilation failed"
        exit 1
    fi
else
    echo "❌ LaTeX not found"
    exit 1
fi

# Test Git
echo -n "🌿 Git: "
if command -v git >/dev/null 2>&1; then
    version=$(git --version | cut -d' ' -f3)
    echo "✅ v$version"
else
    echo "❌ Git not found"
    exit 1
fi

# Check available disk space
echo ""
echo "💾 Disk Usage:"
df -h / | tail -1 | awk '{print "   Root filesystem: " $3 " used / " $2 " total (" $5 " full)"}'

echo ""
echo "🎉 All tests passed! Development environment is ready."
echo "📝 You can now:"
echo "   - Work with Clojure projects using 'clj' or 'lein'"
echo "   - Process LaTeX documents with 'pdflatex'"
echo "   - Lint Clojure code with 'clj-kondo'"
echo "   - Develop ClojureScript with Node.js"