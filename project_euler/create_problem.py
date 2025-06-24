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
        tuple: (problem_title, problem_content, html_content)
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
            return None, None, None
            
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
            return problem_title, None, None
            
        # Get both text and HTML content
        problem_content = content_element.text.strip()
        html_content = str(content_element)
        
        return problem_title, problem_content, html_content
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching problem {problem_number}: {e}")
        return None, None, None

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
(ns proj.p{problem_number}.core
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

def create_tex_file(problem_number, problem_title, problem_content, html_content, folder_path):
    """
    Create a TeX template file for the problem.
    
    Args:
        problem_number: The problem number
        problem_title: The title of the problem
        problem_content: The text content/description of the problem
        html_content: The HTML content of the problem for conversion
        folder_path: Path to the problem folder
    """
    file_path = os.path.join(folder_path, f"p{problem_number}.tex")
    
    # Process the HTML content if available, otherwise use text content
    if html_content:
        latex_content = html_to_latex(html_content)
    elif problem_content:
        # Basic LaTeX escaping
        latex_content = problem_content
        for char in ['&', '%', '$', '#', '_', '{', '}', '~', '^', '\\']:
            if char in latex_content:
                latex_content = latex_content.replace(char, f'\\{char}')
        
        # Replace consecutive newlines with a single LaTeX newline
        latex_content = re.sub(r'\n+', r'\\\\\n', latex_content)
    else:
        latex_content = "Problem content not available. Please visit https://projecteuler.net/problem=" + str(problem_number)
    
    template = f"""\\documentclass{{article}}
\\input{{../shared_preamble}}

\\title{{Project Euler - Problem {problem_number}}}
\\author{{Solution}}
\\date{{{datetime.now().strftime('%Y-%m-%d')}}}

\\begin{{document}}

\\maketitle

\\section*{{Problem {problem_number}: {problem_title}}}

{latex_content}

\\section*{{Solution}}

% TODO: Document your solution approach here

\\section*{{Implementation}}

% TODO: Explain key parts of your implementation

\\end{{document}}
"""
    
    with open(file_path, 'w') as f:
        f.write(template)
    
    print(f"Created TeX file: {file_path}")

def html_to_latex(html_content):
    """
    Convert HTML content to LaTeX format.
    
    Args:
        html_content: HTML content to convert
        
    Returns:
        str: Converted LaTeX content
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Helper function to escape LaTeX special characters in text
    def escape_latex(text):
        # First convert common HTML entities
        html_entities = {
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&',
            '&quot;': '"',
            '&apos;': "'",
            '&nbsp;': ' '
        }
        for entity, replacement in html_entities.items():
            text = text.replace(entity, replacement)
            
        return text
    
    # Process the HTML content
    # Replace <p> tags with paragraph breaks
    for p in soup.find_all('p'):
        p_text = escape_latex(p.get_text())
        p.replace_with(f"{p_text}\n\n")
    
    # Convert <strong> or <b> to LaTeX bold
    for tag in soup.find_all(['strong', 'b']):
        tag.replace_with(f"\\textbf{{{escape_latex(tag.get_text())}}}")
    
    # Convert <em> or <i> to LaTeX italic
    for tag in soup.find_all(['em', 'i']):
        tag.replace_with(f"\\textit{{{escape_latex(tag.get_text())}}}")
    
    # Convert <sup> to LaTeX superscript
    for tag in soup.find_all('sup'):
        tag.replace_with(f"$^{{{escape_latex(tag.get_text())}}}$")
    
    # Convert <sub> to LaTeX subscript
    for tag in soup.find_all('sub'):
        tag.replace_with(f"$_{{{escape_latex(tag.get_text())}}}$")
    
    # Convert <ol> and <ul> lists
    for ol in soup.find_all('ol'):
        items = []
        for li in ol.find_all('li'):
            items.append(f"\\item {escape_latex(li.get_text())}")
        ol_text = "\\begin{enumerate}\n" + "\n".join(items) + "\n\\end{enumerate}"
        ol.replace_with(ol_text)
    
    for ul in soup.find_all('ul'):
        items = []
        for li in ul.find_all('li'):
            items.append(f"\\item {escape_latex(li.get_text())}")
        ul_text = "\\begin{itemize}\n" + "\n".join(items) + "\n\\end{itemize}"
        ul.replace_with(ul_text)
    
    # Handle tables
    for table in soup.find_all('table'):
        rows = table.find_all('tr')
        if not rows:
            continue
            
        # Determine number of columns from the first row
        first_row = rows[0]
        cols = len(first_row.find_all(['th', 'td']))
        
        if cols == 0:
            continue
            
        # Create LaTeX table
        table_lines = [
            "\\begin{center}",
            "\\begin{tabular}{" + "|c" * cols + "|}",
            "\\hline"
        ]
        
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if cells:
                cell_texts = [escape_latex(cell.get_text().strip()) for cell in cells]
                table_lines.append(" & ".join(cell_texts) + " \\\\")
                table_lines.append("\\hline")
                
        table_lines.append("\\end{tabular}")
        table_lines.append("\\end{center}")
        
        table.replace_with("\n".join(table_lines))
    
    # Handle images - convert to LaTeX figure
    for img in soup.find_all('img'):
        alt_text = escape_latex(img.get('alt', 'Image'))
        src = img.get('src', '')
        
        # For Project Euler, we can't download images, so we'll just add a note
        img_text = (
            "\\begin{center}\n"
            f"[Image: {alt_text}]\n\n"
            f"Note: Please refer to the original problem for this image at projecteuler.net\n"
            "\\end{center}"
        )
        img.replace_with(img_text)
    
    # Handle math expressions (often in <span class="math">)
    for math in soup.find_all('span', class_='math'):
        math_text = math.get_text()
        # Don't escape math content as it may contain LaTeX already
        math.replace_with(f"${math_text}$")
    
    # Handle code blocks
    for code in soup.find_all('code'):
        code_text = escape_latex(code.get_text())
        code.replace_with(f"\\texttt{{{code_text}}}")
    
    # Handle blockquotes
    for blockquote in soup.find_all('blockquote'):
        quote_text = escape_latex(blockquote.get_text())
        blockquote.replace_with(f"\\begin{{quote}}\n{quote_text}\n\\end{{quote}}")
    
    # Get the text content - at this point, all HTML has been converted to LaTeX
    content = soup.get_text()
    
    # Clean up excessive newlines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Replace remaining double newlines with paragraph breaks
    content = content.replace('\n\n', '\n\n\\par\n')
    
    return content

def create_test_file(problem_number, folder_path):
    """
    Create a test template file for the problem.
    
    Args:
        problem_number: The problem number
        folder_path: Path to the problem folder
    """
    # Create test directory if it doesn't exist
    test_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proj", "test", "proj")
    test_dir = f"p{problem_number}"
    test_folder_path = os.path.join(test_base_path, test_dir)
    os.makedirs(test_folder_path, exist_ok=True)
    
    file_path = os.path.join(test_folder_path, "core_test.clj")
    
    template = f"""(ns proj.p{problem_number}.core-test
  #_{{:clj-kondo/ignore [:refer-all]}}
  (:require [clojure.test :refer [deftest is testing]]
            [proj.p{problem_number}.core :refer :all]))

(deftest solve-test
  (testing "Testing solution"
    ;; TODO: Add test cases
    (is (= nil (solve)))))
"""
    
    with open(file_path, 'w') as f:
        f.write(template)
    
    print(f"Created test file: {file_path}")

def update_problems_edn(problem_number):
    """
    Update the problems.edn file to include the new problem.
    
    Args:
        problem_number: The problem number to add
    """
    edn_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "proj", "src", "proj", "problems.edn")
    
    try:
        with open(edn_path, 'r') as f:
            content = f.read()
            
        # Parse the EDN content - simple regex since we know the format
        problems_match = re.search(r':problems \[(.*?)\]', content)
        if not problems_match:
            print("Error: Could not find :problems vector in problems.edn")
            return
            
        problems_str = problems_match.group(1).strip()
        problems = sorted(set([int(p) for p in problems_str.split() if p] + [problem_number]))
        new_problems_str = ' '.join(map(str, problems))
        
        # Update the content
        new_content = re.sub(r':problems \[.*?\]', f':problems [{new_problems_str}]', content)
        
        # Write the updated content back
        with open(edn_path, 'w') as f:
            f.write(new_content)
        
        print(f"Updated problems list in: {edn_path}")
        
    except FileNotFoundError:
        # Create new problems.edn file if it doesn't exist
        content = f'{{:problems [{problem_number}]}}'
        os.makedirs(os.path.dirname(edn_path), exist_ok=True)
        with open(edn_path, 'w') as f:
            f.write(content)
        print(f"Created problems.edn file at: {edn_path}")

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
        problem_title, problem_content, html_content = get_problem_info(problem_number)
        
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
        create_tex_file(problem_number, problem_title, problem_content, html_content, folder_path)
        
        # Create the test file
        create_test_file(problem_number, folder_path)
        
        # Update the problems.edn file
        update_problems_edn(problem_number)
        
        print(f"\nSetup complete for Problem {problem_number}: {problem_title}")
        print(f"You can now start working on the solution in {folder_path}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()