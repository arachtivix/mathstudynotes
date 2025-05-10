#!/usr/bin/env python3
"""
Script to start a Clojure REPL with a Project Euler solution loaded.
This script shows the five most recently updated problem directories
and prompts the user to select one before starting the REPL.
"""

import os
import sys
import subprocess
from datetime import datetime
import re

def get_problem_directories():
    """
    Get all problem directories in the project.
    
    Returns:
        list: List of problem directory names (e.g., 'p1', 'p2', etc.)
    """
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proj", "src", "proj")
    problem_dirs = []
    
    for item in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, item)) and re.match(r'^p\d+$', item):
            problem_dirs.append(item)
            
    return problem_dirs

def get_recent_problems(limit=5):
    """
    Get the most recently updated problem directories.
    
    Args:
        limit: Number of recent problems to return
        
    Returns:
        list: List of tuples (problem_dir, last_modified_time)
    """
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proj", "src", "proj")
    problem_dirs = get_problem_directories()
    
    # Get last modified time for each problem directory
    problem_times = []
    for problem_dir in problem_dirs:
        dir_path = os.path.join(base_path, problem_dir)
        
        # Check the modification time of core.clj file
        core_file = os.path.join(dir_path, "core.clj")
        if os.path.exists(core_file):
            mod_time = os.path.getmtime(core_file)
            problem_times.append((problem_dir, mod_time))
    
    # Sort by modification time (most recent first)
    problem_times.sort(key=lambda x: x[1], reverse=True)
    
    # Return the top N problems
    return problem_times[:limit]

def extract_problem_number(problem_dir):
    """
    Extract the problem number from a directory name.
    
    Args:
        problem_dir: Directory name (e.g., 'p123')
        
    Returns:
        int: Problem number
    """
    match = re.match(r'^p(\d+)$', problem_dir)
    if match:
        return int(match.group(1))
    return None

def start_repl_with_problem(problem_number):
    """
    Start a Clojure REPL with the specified problem loaded.
    
    Args:
        problem_number: The problem number to load
    """
    # Change to the project directory
    proj_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proj")
    os.chdir(proj_dir)
    
    # Create a temporary file with REPL initialization commands
    init_file = os.path.join(proj_dir, "temp_repl_init.clj")
    with open(init_file, 'w') as f:
        f.write(f"""
;; Load the problem namespace
(require '[p{problem_number}.core :as p{problem_number}])

;; Run the solution
(println "\\nRunning solution for Problem {problem_number}:")
(println "-----------------------------------------")
(p{problem_number}/-main)
(println "-----------------------------------------")
(println "REPL is now ready. The problem namespace is loaded as p{problem_number}")
(println "You can access functions from the solution with p{problem_number}/function-name")
(println "Example: (p{problem_number}/solve)")
""")
    
    try:
        # Start the REPL with the initialization file
        print(f"\nStarting Clojure REPL with Problem {problem_number} loaded...")
        subprocess.run(["lein", "repl", ":init", init_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting REPL: {e}")
    except KeyboardInterrupt:
        print("\nREPL terminated by user.")
    finally:
        # Clean up the temporary file
        if os.path.exists(init_file):
            os.remove(init_file)

def main():
    """Main function to start the REPL with a selected problem."""
    try:
        # Get recent problems
        recent_problems = get_recent_problems()
        
        if not recent_problems:
            print("No problem directories found.")
            return
        
        # Display recent problems
        print("Five most recently updated Project Euler problems:")
        print("--------------------------------------------------")
        for i, (problem_dir, mod_time) in enumerate(recent_problems, 1):
            problem_number = extract_problem_number(problem_dir)
            mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{i}. Problem {problem_number} (Last modified: {mod_time_str})")
        
        print("\nEnter a number from the list above, or any other Project Euler problem number:")
        choice = input("> ").strip()
        
        # Process the user's choice
        problem_number = None
        
        if choice.isdigit():
            choice_num = int(choice)
            
            # Check if the choice is from the list
            if 1 <= choice_num <= len(recent_problems):
                problem_dir = recent_problems[choice_num - 1][0]
                problem_number = extract_problem_number(problem_dir)
            else:
                # Assume the user entered a problem number directly
                problem_number = choice_num
        
        if not problem_number:
            print("Invalid choice. Please enter a valid number.")
            return
        
        # Check if the problem directory exists
        problem_dir = f"p{problem_number}"
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proj", "src", "proj")
        if not os.path.exists(os.path.join(base_path, problem_dir)):
            print(f"Problem {problem_number} does not exist in the project.")
            create_new = input(f"Would you like to create Problem {problem_number}? (y/n): ").strip().lower()
            if create_new == 'y':
                # Run the create_problem.py script
                script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "create_problem.py")
                process = subprocess.Popen([sys.executable, script_path], stdin=subprocess.PIPE, 
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                          universal_newlines=True)
                stdout, stderr = process.communicate(input=f"{problem_number}\n")
                print(stdout)
                if process.returncode != 0:
                    print(f"Error creating problem: {stderr}")
                    return
            else:
                return
        
        # Start the REPL with the selected problem
        start_repl_with_problem(problem_number)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()