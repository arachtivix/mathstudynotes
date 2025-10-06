#!/usr/bin/env python3
"""
Script to analyze all root LaTeX documents and generate the master documents.json catalog.
"""

import os
import re
import json
from pathlib import Path

def extract_latex_metadata(tex_file_path):
    """Extract title, author, and other metadata from a LaTeX file."""
    metadata = {
        "title": None,
        "author": None,
        "documentclass": None
    }
    
    try:
        with open(tex_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Extract document class
        doc_class_match = re.search(r'\\documentclass(?:\[.*?\])?\{(.*?)\}', content)
        if doc_class_match:
            metadata["documentclass"] = doc_class_match.group(1)
            
        # Extract title
        title_match = re.search(r'\\title\{(.*?)\}', content, re.DOTALL)
        if title_match:
            metadata["title"] = title_match.group(1).strip()
            
        # Extract author  
        author_match = re.search(r'\\author\{(.*?)\}', content, re.DOTALL)
        if author_match:
            metadata["author"] = author_match.group(1).strip()
            
    except Exception as e:
        print(f"Warning: Could not read {tex_file_path}: {e}")
        
    return metadata

def determine_subject_and_type(file_path):
    """Determine subject area and document type from file path."""
    path_parts = Path(file_path).parts
    
    # Determine subject area
    subject = "miscellaneous"
    if "concrete_math" in path_parts:
        subject = "concrete_math"
    elif "aocp_v1" in path_parts:
        subject = "aocp_v1"
    elif "project_euler" in path_parts:
        subject = "project_euler"
    elif "unbound" in path_parts:
        subject = "unbound"
    elif "onag" in path_parts:
        subject = "onag"
    elif "templates" in path_parts:
        subject = "templates"
        
    # Determine document type
    doc_type = "document"
    filename = Path(file_path).name.lower()
    
    if "writeup" in filename:
        doc_type = "writeup"
    elif "problem" in filename or filename.startswith("p") and filename[1:].split('.')[0].isdigit():
        doc_type = "problem"
    elif "overview" in filename:
        doc_type = "overview"
    elif "solution" in filename:
        doc_type = "solution"
    elif "template" in filename:
        doc_type = "template"
    elif "demo" in filename:
        doc_type = "demo"
    elif "notes" in filename:
        doc_type = "notes"
    elif "analysis" in filename:
        doc_type = "analysis"
        
    return subject, doc_type

def find_dependencies(tex_file_path, repo_root):
    """Find dependencies like shared preambles or input files."""
    dependencies = []
    
    try:
        with open(tex_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Look for \input{} commands
        input_matches = re.findall(r'\\input\{(.*?)\}', content)
        for input_file in input_matches:
            if not input_file.endswith('.tex'):
                input_file += '.tex'
            dependencies.append(input_file)
            
        # Look for \include{} commands  
        include_matches = re.findall(r'\\include\{(.*?)\}', content)
        for include_file in include_matches:
            if not include_file.endswith('.tex'):
                include_file += '.tex'
            dependencies.append(include_file)
            
    except Exception as e:
        print(f"Warning: Could not analyze dependencies for {tex_file_path}: {e}")
        
    return dependencies

def generate_documents_catalog():
    """Generate the complete documents catalog."""
    repo_root = Path(__file__).parent.parent
    
    # Find all root LaTeX documents
    root_docs = []
    for tex_file in repo_root.rglob("*.tex"):
        try:
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if r'\documentclass' in content:
                    root_docs.append(tex_file)
        except Exception as e:
            print(f"Warning: Could not check {tex_file}: {e}")
            
    print(f"Found {len(root_docs)} root LaTeX documents")
    
    # Build catalog
    catalog = {
        "metadata": {
            "generated": "2024-01-01",  # Will be updated by actual generation
            "description": "Master catalog of all root LaTeX documents in the mathstudynotes repository",
            "total_documents": len(root_docs)
        },
        "documents": {}
    }
    
    # Group documents by subject
    for tex_file in sorted(root_docs):
        rel_path = tex_file.relative_to(repo_root)
        subject, doc_type = determine_subject_and_type(str(rel_path))
        
        # Extract metadata
        metadata = extract_latex_metadata(tex_file)
        dependencies = find_dependencies(tex_file, repo_root)
        
        # Create document entry
        doc_entry = {
            "path": str(rel_path),
            "title": metadata["title"] or rel_path.stem,
            "author": metadata["author"],
            "subject": subject,
            "type": doc_type,
            "documentclass": metadata["documentclass"],
            "dependencies": dependencies
        }
        
        # Add to catalog grouped by subject
        if subject not in catalog["documents"]:
            catalog["documents"][subject] = []
        catalog["documents"][subject].append(doc_entry)
    
    return catalog

if __name__ == "__main__":
    catalog = generate_documents_catalog()
    
    # Write to documents.json
    output_file = Path(__file__).parent / "documents.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        
    print(f"Generated documents catalog: {output_file}")
    print(f"Total documents: {catalog['metadata']['total_documents']}")
    
    # Print summary by subject
    print("\nDocuments by subject:")
    for subject, docs in catalog["documents"].items():
        print(f"  {subject}: {len(docs)} documents")