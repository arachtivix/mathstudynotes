#!/usr/bin/env python3
"""
Script to render LaTeX files for Project Euler problems.
Provides a menu-based interface to select and compile LaTeX files.
"""

import os
import glob
import subprocess
import json
from datetime import datetime

# File to store the last rendered file information
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".latex_history.json")

def load_history():
    """Load the rendering history from file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"last_rendered": None}
    return {"last_rendered": None}

def save_history(file_path):
    """Save the last rendered file to history."""
    history = {"last_rendered": file_path}
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def get_project_structure():
    """Get the structure of LaTeX files in the project."""
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proj", "src", "proj")
    print(f"\nScanning for LaTeX files in: {base_path}")
    
    if not os.path.exists(base_path):
        print(f"Warning: Base path does not exist: {base_path}")
        print("Creating directory structure...")
        os.makedirs(base_path, exist_ok=True)
        return {}
    
    # Find all problem directories
    print("Looking for problem directories...")
    problem_dirs = sorted(glob.glob(os.path.join(base_path, "p*")))
    if not problem_dirs:
        print("No problem directories found matching pattern 'p*'")
        return {}
    
    # Collect all LaTeX files
    tex_files = {}
    print(f"\nFound {len(problem_dirs)} problem directories")
    for dir_path in problem_dirs:
        dir_name = os.path.basename(dir_path)
        print(f"Scanning {dir_name}...", end=" ")
        tex_files_in_dir = glob.glob(os.path.join(dir_path, "*.tex"))
        if tex_files_in_dir:
            tex_files[dir_name] = tex_files_in_dir
            print(f"found {len(tex_files_in_dir)} LaTeX files")
        else:
            print("no LaTeX files found")
            
    return tex_files

def render_latex(tex_file):
    """
    Render a LaTeX file using pdflatex.
    
    Args:
        tex_file: Path to the LaTeX file
    
    Returns:
        bool: True if compilation was successful, False otherwise
    """
    try:
        # Get the directory containing the tex file
        working_dir = os.path.dirname(tex_file)
        print(f"\nPreparing to render {os.path.basename(tex_file)}")
        print(f"Working directory: {working_dir}")
        
        if not os.path.exists(tex_file):
            print(f"Error: LaTeX file does not exist: {tex_file}")
            return False
            
        # Run pdflatex twice to resolve references
        for pass_num in range(2):
            print(f"\nLaTeX compilation pass {pass_num + 1}/2...")
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', os.path.basename(tex_file)],
                cwd=working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check for common LaTeX errors in output
            output = result.stdout
            if "! LaTeX Error:" in output:
                print("LaTeX Error detected in output:")
                error_start = output.find("! LaTeX Error:")
                error_end = output.find("\n", error_start + 100)
                print(output[error_start:error_end])
                return False
                
            if result.returncode != 0:
                print(f"Error during LaTeX compilation (pass {pass_num + 1}):")
                if result.stderr:
                    print(result.stderr)
                else:
                    print("No error output available. Check if pdflatex is installed.")
                return False
            
            print(f"Pass {pass_num + 1} completed successfully")
                
        pdf_file = os.path.splitext(tex_file)[0] + '.pdf'
        if os.path.exists(pdf_file):
            print(f"\nSuccessfully rendered {os.path.basename(tex_file)}")
            print(f"PDF file created: {pdf_file}")
            return True
        else:
            print(f"\nWarning: PDF file was not created at expected location: {pdf_file}")
            return False
        
    except FileNotFoundError:
        print("Error: pdflatex command not found. Please ensure LaTeX is installed.")
        return False
    except Exception as e:
        print(f"Error rendering LaTeX file: {e}")
        import traceback
        traceback.print_exc()
        return False

def display_menu(tex_files, history):
    """Display the menu and handle user input."""
    while True:
        print("\nProject Euler LaTeX Renderer")
        print("=" * 30)
        
        # Show the last rendered file if it exists
        if history["last_rendered"]:
            print(f"\nLast rendered: {os.path.basename(history['last_rendered'])}")
            print("Press Enter to re-render the last file, or choose from below:")
            
        print("\nAvailable problems:")
        problems = sorted(tex_files.keys())
        for i, problem in enumerate(problems, 1):
            print(f"{i}. {problem}")
        
        print("\nq. Quit")
        
        choice = input("\nSelect a problem (or press Enter for last rendered): ").strip()
        
        if choice.lower() == 'q':
            break
            
        if not choice and history["last_rendered"]:
            # Re-render the last file
            render_latex(history["last_rendered"])
            continue
            
        try:
            if choice:
                idx = int(choice) - 1
                if 0 <= idx < len(problems):
                    problem = problems[idx]
                    tex_files_in_dir = tex_files[problem]
                    
                    if len(tex_files_in_dir) == 1:
                        # If there's only one file, render it directly
                        tex_file = tex_files_in_dir[0]
                        if render_latex(tex_file):
                            save_history(tex_file)
                    else:
                        # Show submenu for multiple files
                        print(f"\nFiles in {problem}:")
                        for i, tex_file in enumerate(tex_files_in_dir, 1):
                            print(f"{i}. {os.path.basename(tex_file)}")
                            
                        sub_choice = input("\nSelect a file to render: ").strip()
                        try:
                            sub_idx = int(sub_choice) - 1
                            if 0 <= sub_idx < len(tex_files_in_dir):
                                tex_file = tex_files_in_dir[sub_idx]
                                if render_latex(tex_file):
                                    save_history(tex_file)
                        except ValueError:
                            print("Invalid selection")
                else:
                    print("Invalid problem number")
        except ValueError:
            print("Invalid input")

def main():
    """Main function to run the LaTeX renderer."""
    try:
        print("\nProject Euler LaTeX Renderer")
        print("=" * 30)
        print("\nInitializing...")
        
        print("Loading rendering history...")
        history = load_history()
        if history["last_rendered"]:
            print(f"Last rendered file: {history['last_rendered']}")
        else:
            print("No previous rendering history found")
        
        print("\nScanning project structure...")
        tex_files = get_project_structure()
        
        if not tex_files:
            print("\nNo LaTeX files found in the project.")
            print("Expected structure: proj/src/proj/p*/")
            print("Each problem directory (p*) should contain .tex files")
            return
            
        print(f"\nFound {sum(len(files) for files in tex_files.values())} LaTeX files in {len(tex_files)} problem directories")
        display_menu(tex_files, history)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("\nDetailed error information:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()