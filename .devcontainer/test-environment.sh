#!/bin/bash
# Electric Underpants Dev Environment Test Script
# Run this to verify your development environment is working correctly

echo "🩲⚡ Testing Electric Underpants Dev Environment..."
echo

FAILED=0

# Test Java
echo "Testing Java..."
if java --version >/dev/null 2>&1; then
    echo "✅ Java: $(java --version | head -1)"
else
    echo "❌ Java not found"
    FAILED=1
fi

# Test Node.js  
echo "Testing Node.js..."
if node --version >/dev/null 2>&1; then
    echo "✅ Node.js: $(node --version)"
else
    echo "❌ Node.js not found"
    FAILED=1
fi

# Test Clojure CLI
echo "Testing Clojure CLI..."
if clojure --version >/dev/null 2>&1; then
    echo "✅ Clojure CLI: $(clojure --version)"
else
    echo "❌ Clojure CLI not found"
    FAILED=1
fi

# Test Leiningen
echo "Testing Leiningen..."
if lein --version >/dev/null 2>&1; then
    echo "✅ Leiningen: $(lein --version | head -1)"
else
    echo "❌ Leiningen not found"
    FAILED=1
fi

# Test clj-kondo
echo "Testing clj-kondo..."
if clj-kondo --version >/dev/null 2>&1; then
    echo "✅ clj-kondo: $(clj-kondo --version)"
else
    echo "❌ clj-kondo not found"
    FAILED=1
fi

# Test LaTeX
echo "Testing LaTeX..."
if pdflatex --version >/dev/null 2>&1; then
    echo "✅ LaTeX: pdflatex available"
else
    echo "❌ LaTeX not found"
    FAILED=1
fi

echo

if [ $FAILED -eq 0 ]; then
    echo "🎉 All tests passed! Electric Underpants environment is ready!"
    echo
    echo "Try these commands to get started:"
    echo "  cd unbound/hand_numbers && lein repl"
    echo "  cd chess/chessoids && clojure -M:dev"
    echo "  cd winning_ways/cutcake && lein run"
    echo "  pdflatex test.tex"
else
    echo "❌ Some tools are missing. Check the setup-clojure.sh script."
    exit 1
fi