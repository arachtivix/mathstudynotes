#!/usr/bin/env python3
"""
Build status tracking system for LaTeX documents in the project.
This module extends the render_latex.py functionality to track and report
build status for all documents listed in problems.edn.
"""

import os
import json
import edn_format
from datetime import datetime
from render_latex import get_project_structure, render_latex


def load_problems_list():
    """Load the master list of problems from problems.edn."""
    problems_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "proj", "src", "proj", "problems.edn"
    )
    
    if not os.path.exists(problems_file):
        print(f"Warning: problems.edn not found at {problems_file}")
        return {"problems": []}
    
    try:
        with open(problems_file, 'r') as f:
            content = f.read()
            data = edn_format.loads(content)
            # EDN uses Keywords, convert to regular dict
            problems_key = edn_format.Keyword("problems")
            problems = data.get(problems_key, [])
            return {"problems": problems}
    except Exception as e:
        print(f"Error reading problems.edn: {e}")
        return {"problems": []}


def get_build_status_file():
    """Get the path to the build status JSON file."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "proj", "src", "proj", "build_status.json"
    )


def load_build_status():
    """Load the current build status from JSON file."""
    status_file = get_build_status_file()
    if os.path.exists(status_file):
        try:
            with open(status_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading build status: {e}")
    
    return {
        "last_updated": None,
        "problems": {}
    }


def save_build_status(status_data):
    """Save the build status to JSON file."""
    status_file = get_build_status_file()
    status_data["last_updated"] = datetime.now().isoformat()
    
    try:
        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        print(f"Error saving build status: {e}")


def build_all_documents(dry_run=False):
    """
    Build all documents and track their status.
    Returns a dictionary with build results.
    
    Args:
        dry_run: If True, simulate builds without actually running LaTeX
    """
    print("Building all documents and tracking status...")
    if dry_run:
        print("(Running in dry-run mode - no actual LaTeX compilation)")
    
    # Load the master list
    problems_data = load_problems_list()
    master_problems = problems_data.get("problems", [])
    
    # Get current project structure
    tex_files = get_project_structure()
    
    # Load existing build status
    status_data = load_build_status()
    
    build_results = {}
    
    for problem_num in master_problems:
        problem_dir = f"p{problem_num}"
        print(f"\nProcessing problem {problem_num} (directory: {problem_dir})...")
        
        if problem_dir not in tex_files:
            print(f"  No LaTeX files found for problem {problem_num}")
            build_results[problem_num] = {
                "status": "missing",
                "message": "No LaTeX files found",
                "timestamp": datetime.now().isoformat(),
                "files": []
            }
            continue
        
        problem_files = tex_files[problem_dir]
        file_results = []
        overall_success = True
        
        for tex_file in problem_files:
            print(f"  Building {os.path.basename(tex_file)}...")
            
            if dry_run:
                # Simulate build - just check if file exists and has content
                success = os.path.exists(tex_file) and os.path.getsize(tex_file) > 0
                if success:
                    print(f"    [DRY RUN] Would compile {os.path.basename(tex_file)}")
                else:
                    print(f"    [DRY RUN] File issues with {os.path.basename(tex_file)}")
            else:
                success = render_latex(tex_file)
            
            file_results.append({
                "file": os.path.basename(tex_file),
                "path": tex_file,
                "success": success
            })
            
            if not success:
                overall_success = False
        
        build_results[problem_num] = {
            "status": "success" if overall_success else "failed",
            "message": f"Built {len([f for f in file_results if f['success']])} of {len(file_results)} files successfully",
            "timestamp": datetime.now().isoformat(),
            "files": file_results
        }
    
    # Update status data
    status_data["problems"] = build_results
    save_build_status(status_data)
    
    return build_results


def generate_status_report():
    """Generate a human-readable status report."""
    status_data = load_build_status()
    problems_data = load_problems_list()
    master_problems = problems_data.get("problems", [])
    
    print("\n" + "="*60)
    print("PROJECT EULER DOCUMENT BUILD STATUS REPORT")
    print("="*60)
    
    if status_data.get("last_updated"):
        print(f"Last updated: {status_data['last_updated']}")
    else:
        print("No build status available")
        return
    
    problems_status = status_data.get("problems", {})
    
    success_count = 0
    failed_count = 0
    missing_count = 0
    
    print(f"\nMaster list contains {len(master_problems)} problems")
    print("\nDetailed Status:")
    print("-" * 60)
    
    for problem_num in sorted(master_problems):
        if str(problem_num) in problems_status:
            problem_status = problems_status[str(problem_num)]
            status = problem_status.get("status", "unknown")
            message = problem_status.get("message", "")
            
            status_symbol = {
                "success": "✓",
                "failed": "✗", 
                "missing": "?"
            }.get(status, "?")
            
            print(f"Problem {problem_num:3d}: [{status_symbol}] {status.upper():8s} - {message}")
            
            if status == "success":
                success_count += 1
            elif status == "failed":
                failed_count += 1
            elif status == "missing":
                missing_count += 1
        else:
            print(f"Problem {problem_num:3d}: [?] UNKNOWN   - No build data available")
    
    print("-" * 60)
    print(f"Summary: {success_count} successful, {failed_count} failed, {missing_count} missing")
    if len(master_problems) > 0:
        print(f"Success rate: {(success_count / len(master_problems) * 100):.1f}%")
    else:
        print("Success rate: N/A (no problems in master list)")


def generate_status_markdown():
    """Generate a markdown status summary."""
    status_data = load_build_status()
    problems_data = load_problems_list()
    master_problems = problems_data.get("problems", [])
    
    if not status_data.get("last_updated"):
        return "# Build Status\n\nNo build status available.\n"
    
    problems_status = status_data.get("problems", {})
    
    success_count = 0
    failed_count = 0
    missing_count = 0
    
    # Count statuses
    for problem_num in master_problems:
        if str(problem_num) in problems_status:
            status = problems_status[str(problem_num)].get("status", "unknown")
            if status == "success":
                success_count += 1
            elif status == "failed":
                failed_count += 1
            elif status == "missing":
                missing_count += 1
    
    # Generate markdown
    md_lines = [
        "# LaTeX Document Build Status",
        "",
        f"**Last updated:** {status_data['last_updated']}",
        "",
        f"**Total problems:** {len(master_problems)}",
        f"- ✓ **{success_count}** successful builds",
        f"- ✗ **{failed_count}** failed builds", 
        f"- ? **{missing_count}** missing files",
        ""
    ]
    
    if len(master_problems) > 0:
        success_rate = (success_count / len(master_problems) * 100)
        md_lines.append(f"**Success rate:** {success_rate:.1f}%")
        md_lines.append("")
    
    # Add detailed status table
    md_lines.extend([
        "## Detailed Status",
        "",
        "| Problem | Status | Message |",
        "|---------|--------|---------|"
    ])
    
    for problem_num in sorted(master_problems):
        if str(problem_num) in problems_status:
            problem_status = problems_status[str(problem_num)]
            status = problem_status.get("status", "unknown")
            message = problem_status.get("message", "")
            
            status_symbol = {
                "success": "✓",
                "failed": "✗", 
                "missing": "?"
            }.get(status, "?")
            
            md_lines.append(f"| {problem_num} | {status_symbol} {status} | {message} |")
        else:
            md_lines.append(f"| {problem_num} | ? unknown | No build data available |")
    
    return "\n".join(md_lines) + "\n"


def save_status_markdown():
    """Save the status summary as a markdown file."""
    md_content = generate_status_markdown()
    md_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "BUILD_STATUS.md"
    )
    
    try:
        with open(md_file, 'w') as f:
            f.write(md_content)
        print(f"\nStatus summary saved to: {md_file}")
    except Exception as e:
        print(f"Error saving status markdown: {e}")


def main():
    """Main function for build status operations."""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "build":
            build_all_documents()
        elif command == "build-dry-run":
            build_all_documents(dry_run=True)
        elif command == "report":
            generate_status_report()
        elif command == "build-and-report":
            build_all_documents()
            generate_status_report()
        elif command == "dry-run-and-report":
            build_all_documents(dry_run=True)
            generate_status_report()
            save_status_markdown()
        elif command == "markdown":
            save_status_markdown()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: build, report, build-and-report")
    else:
        print("Build Status Tracker for Project Euler LaTeX Documents")
        print("Usage: python build_status.py [command]")
        print("Commands:")
        print("  build            - Build all documents and update status")
        print("  build-dry-run    - Simulate builds without LaTeX compilation")
        print("  report           - Generate status report")
        print("  build-and-report - Build all documents and generate report")
        print("  dry-run-and-report - Simulate builds and generate report")
        print("  markdown         - Generate markdown status summary")


if __name__ == "__main__":
    main()