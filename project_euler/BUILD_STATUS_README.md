# LaTeX Build Status System

This system tracks the build status of all LaTeX documents listed in the master list (`proj/src/proj/problems.edn`).

## Files

- `build_status.py` - Main script for tracking build status
- `proj/src/proj/build_status.json` - JSON file storing current build status
- `proj/src/proj/problems.edn` - Master list of problems (EDN format)
- `.github/workflows/latex-build-status.yml` - GitHub workflow for automated builds

## Usage

### Command Line

```bash
# Run build status check with real LaTeX compilation
python build_status.py build

# Simulate builds without LaTeX (useful for testing)
python build_status.py build-dry-run

# Generate status report only
python build_status.py report

# Build and generate report in one command
python build_status.py build-and-report

# Dry run and generate report (for testing)
python build_status.py dry-run-and-report
```

### Status Information

The system tracks:
- **Success**: Document compiled successfully
- **Failed**: LaTeX compilation failed
- **Missing**: No LaTeX files found for problem in master list

For each document, the system stores:
- Build timestamp
- Success/failure status
- Detailed file-level results
- Error messages (if any)

### GitHub Workflow

The workflow (`.github/workflows/latex-build-status.yml`) automatically:
1. Runs on pushes to LaTeX files or related scripts
2. Installs LaTeX and Python dependencies
3. Attempts to build all documents
4. Uploads artifacts (PDFs and status)
5. Commits updated status back to repository

### Master List Format

The `problems.edn` file uses EDN format:
```edn
{:problems [3 4 7 9 10 12 15 16 26 28 51 95 123 202 203 204 205 206 361 879]}
```

To add a new problem to track, add its number to the problems vector.

### Status Report Example

```
============================================================
PROJECT EULER DOCUMENT BUILD STATUS REPORT
============================================================
Last updated: 2025-09-01T17:05:11.506856

Master list contains 20 problems

Detailed Status:
------------------------------------------------------------
Problem  26: [✓] SUCCESS  - Built 1 of 1 files successfully
Problem  28: [✓] SUCCESS  - Built 1 of 1 files successfully
Problem 205: [✓] SUCCESS  - Built 2 of 2 files successfully
Problem   3: [?] MISSING  - No LaTeX files found
------------------------------------------------------------
Summary: 10 successful, 0 failed, 10 missing
Success rate: 50.0%
```

## Dependencies

- Python 3.6+
- `edn_format` library (install with `pip install -r requirements.txt`)
- LaTeX distribution (for actual builds)