#!/usr/bin/env python3
"""
Script to create a new Project Euler problem folder with templates.
This script fetches the problem description from projecteuler.net,
extracts the problem name, and creates the necessary files.
"""

import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_problem_info(problem_number):
    """
    Fetch problem information from Project Euler website.
    
    Args:
        problem_number: The problem number to fetch
        
    Returns:
        tuple: (problem_title, problem_content)
    """
    url = f"https://projecteuler.net/problem={problem_number}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the problem title
        title_element = soup.find('h2')
        if not title_element:
            print(f"Error: Could not find problem title for problem {problem_number}")
            return None, None
            
        # The title format is typically "Problem X: Actual Title"
        full_title = title_element.text.strip()
        title_match = re.match(r"Problem \d+: (.*)", full_title)
        if title_match:
            problem_title = title_match.group(1)
        else:
            problem_title = full_title
            
        # Extract the problem content
        content_element = soup.find('div', class_='problem_content')
        if not content_element:
            print(f"Error: Could not find problem content for problem {problem_number}")
            return problem_title, None
            
        problem_content = content_element.text.strip()
        
        return problem_title, problem_content
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching problem {problem_number}: {e}")
        return None, None

def create_clojure_file(problem_number, problem_title, folder_path):
    """
    Create a Clojure template file for the problem.
    
    Args:
        problem_number: The problem number
        problem_title: The title of the problem
        folder_path: Path to the problem folder
    """
    file_path = os.path.join(folder_path, "core.clj")
    
    template = f"""
(ns p{problem_number}.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem {problem_number}: {problem_title}
;; Created on {datetime.now().strftime('%Y-%m-%d')}

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem {problem_number}:")
  (println (solve)))
"""
    
    with open(file_path, 'w') as f:
        f.write(template)
    
    print(f"Created Clojure file: {file_path}")

def create_tex_file(problem_number, problem_title, problem_content, folder_path):
    """
    Create a TeX template file for the problem.
    
    Args:
        problem_number: The problem number
        problem_title: The title of the problem
        problem_content: The content/description of the problem
        folder_path: Path to the problem folder
    """
    file_path = os.path.join(folder_path, f"p{problem_number}.tex")
    
    # Escape special LaTeX characters in the problem content
    if problem_content:
        # Basic LaTeX escaping
        for char in ['&', '%', '$', '#', '_', '{', '}', '~', '^', '\\']:
            if char in problem_content:
                problem_content = problem_content.replace(char, f'\\{char}')
        
        # Replace newlines with LaTeX newlines
        problem_content = problem_content.replace('\n', '\\\\\n')
    else:
        problem_content = "Problem content not available. Please visit https://projecteuler.net/problem=" + str(problem_number)
    
    template = f"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{graphicx}}

\\title{{Project Euler - Problem {problem_number}}}
\\author{{Solution}}
\\date{{{datetime.now().strftime('%Y-%m-%d')}}}

\\begin{{document}}

\\maketitle

\\section*{{Problem {problem_number}: {problem_title}}}

{problem_content}

\\section*{{Solution}}

% TODO: Document your solution approach here

\\section*{{Implementation}}

% TODO: Explain key parts of your implementation

\\end{{document}}
"""
    
    with open(file_path, 'w') as f:
        f.write(template)
    
    print(f"Created TeX file: {file_path}")

def main():
    """Main function to create a new Project Euler problem folder."""
    try:
        problem_number = input("Enter the Project Euler problem number: ").strip()
        
        # Validate input
        if not problem_number.isdigit():
            print("Error: Problem number must be a positive integer")
            return
            
        problem_number = int(problem_number)
        
        # Fetch problem information
        print(f"Fetching problem {problem_number} from Project Euler...")
        problem_title, problem_content = get_problem_info(problem_number)
        
        if not problem_title:
            print(f"Could not retrieve information for problem {problem_number}")
            return
            
        print(f"Problem {problem_number}: {problem_title}")
        
        # Create the problem directory
        base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proj", "src", "proj")
        problem_dir = f"p{problem_number}"
        folder_path = os.path.join(base_path, problem_dir)
        
        if os.path.exists(folder_path):
            overwrite = input(f"Problem folder {problem_dir} already exists. Overwrite? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("Operation cancelled.")
                return
        else:
            os.makedirs(folder_path, exist_ok=True)
            
        print(f"Created problem folder: {folder_path}")
        
        # Create the Clojure file
        create_clojure_file(problem_number, problem_title, folder_path)
        
        # Create the TeX file
        create_tex_file(problem_number, problem_title, problem_content, folder_path)
        
        print(f"\nSetup complete for Problem {problem_number}: {problem_title}")
        print(f"You can now start working on the solution in {folder_path}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()