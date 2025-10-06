#!/usr/bin/env python3
"""
Build script for compiling LaTeX documents from the master catalog.
This is a framework for future LaTeX compilation workflows.
"""

import os
import json
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Any

def load_documents_catalog(catalog_path: Path = None) -> Dict[str, Any]:
    """Load the documents catalog."""
    if catalog_path is None:
        catalog_path = Path(__file__).parent / "documents.json"
    
    with open(catalog_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_documents(catalog: Dict[str, Any], subject: str = None):
    """List all documents, optionally filtered by subject."""
    print("Available LaTeX documents:\n")
    
    subjects = [subject] if subject else sorted(catalog["documents"].keys())
    
    for subj in subjects:
        if subj in catalog["documents"]:
            docs = catalog["documents"][subj]
            print(f"{subj.upper()} ({len(docs)} documents):")
            for i, doc in enumerate(docs, 1):
                print(f"  {i:2d}. {doc['title']}")
                print(f"      Path: {doc['path']}")
                print(f"      Type: {doc['type']}")
                if doc['dependencies']:
                    print(f"      Dependencies: {', '.join(doc['dependencies'])}")
                print()

def check_latex_tools():
    """Check if LaTeX compilation tools are available."""
    tools_status = {}
    
    tools = ['pdflatex', 'latexmk', 'xelatex', 'lualatex']
    
    for tool in tools:
        try:
            result = subprocess.run(['which', tool], 
                                  capture_output=True, text=True)
            tools_status[tool] = result.returncode == 0
        except Exception:
            tools_status[tool] = False
    
    return tools_status

def build_document(doc_entry: Dict[str, Any], repo_root: Path, output_dir: Path):
    """Build a single LaTeX document (placeholder implementation)."""
    tex_path = repo_root / doc_entry['path']
    
    if not tex_path.exists():
        print(f"Error: Document not found: {tex_path}")
        return False
    
    print(f"Building: {doc_entry['title']}")
    print(f"  Source: {tex_path}")
    print(f"  Type: {doc_entry['type']}")
    
    # Check dependencies
    if doc_entry['dependencies']:
        print(f"  Dependencies: {', '.join(doc_entry['dependencies'])}")
        
        # TODO: Verify dependencies exist
        for dep in doc_entry['dependencies']:
            # Dependencies are relative to the tex file's directory
            dep_path = tex_path.parent / dep
            if not dep_path.exists():
                print(f"  Warning: Dependency not found: {dep_path}")
    
    # TODO: Actual LaTeX compilation would go here
    print("  Status: Ready for compilation (LaTeX tools not available)")
    print()
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Build LaTeX documents from the master catalog')
    parser.add_argument('--list', action='store_true', 
                       help='List all available documents')
    parser.add_argument('--subject', type=str,
                       help='Filter by subject area')
    parser.add_argument('--document', type=str,
                       help='Build specific document by path')
    parser.add_argument('--all', action='store_true',
                       help='Build all documents')
    parser.add_argument('--check-tools', action='store_true',
                       help='Check availability of LaTeX tools')
    
    args = parser.parse_args()
    
    # Load catalog
    try:
        catalog = load_documents_catalog()
    except FileNotFoundError:
        print("Error: documents.json not found. Run generate_catalog.py first.")
        return 1
    except Exception as e:
        print(f"Error loading catalog: {e}")
        return 1
    
    repo_root = Path(__file__).parent.parent
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Handle commands
    if args.check_tools:
        tools = check_latex_tools()
        print("LaTeX Tools Status:")
        for tool, available in tools.items():
            status = "✓ Available" if available else "✗ Not found"
            print(f"  {tool}: {status}")
        print()
        
        if not any(tools.values()):
            print("Warning: No LaTeX tools found. Document compilation will not be possible.")
            print("Consider installing LaTeX (e.g., apt install texlive-latex-base texlive-latex-extra)")
        return 0
    
    if args.list:
        list_documents(catalog, args.subject)
        return 0
    
    if args.document:
        # Find and build specific document
        found = False
        for subject_docs in catalog["documents"].values():
            for doc in subject_docs:
                if doc['path'] == args.document or doc['title'] == args.document:
                    build_document(doc, repo_root, output_dir)
                    found = True
                    break
        
        if not found:
            print(f"Error: Document not found: {args.document}")
            return 1
        return 0
    
    if args.all:
        print(f"Building all {catalog['metadata']['total_documents']} documents...\n")
        
        success_count = 0
        for subject, docs in catalog["documents"].items():
            print(f"Building {subject} documents:")
            for doc in docs:
                if build_document(doc, repo_root, output_dir):
                    success_count += 1
        
        print(f"Build summary: {success_count}/{catalog['metadata']['total_documents']} documents processed")
        return 0
    
    # Default: show help and basic info
    print(f"LaTeX Documents Build System")
    print(f"Repository contains {catalog['metadata']['total_documents']} root LaTeX documents")
    print(f"\nUse --help to see all options")
    print(f"Quick start:")
    print(f"  --list              List all documents")
    print(f"  --check-tools       Check LaTeX tool availability")
    print(f"  --all               Build all documents (placeholder)")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())