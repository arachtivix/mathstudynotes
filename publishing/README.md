# Publishing Infrastructure

This directory contains the infrastructure for building and publishing LaTeX documents from this repository.

## Structure

- `documents.json` - Master list of all root LaTeX documents that can be compiled independently
- `build_documents.py` - Build script for compiling LaTeX documents (future implementation)
- `output/` - Generated PDF files will be placed here during builds

## Document Catalog

The `documents.json` file contains metadata for all root LaTeX documents in the repository, organized by subject area. Each document entry includes:

- **path**: Relative path to the .tex file from repository root
- **title**: Document title (extracted from \title{} or filename)
- **author**: Document author (if specified)
- **subject**: Subject area (concrete_math, aocp_v1, project_euler, etc.)
- **type**: Document type (problem, writeup, overview, template, etc.)
- **dependencies**: Any shared files or templates it depends on

This catalog enables automated building and publishing workflows.