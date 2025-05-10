# Project Euler Solutions

This repository contains solutions to [Project Euler](https://projecteuler.net/) problems implemented in Clojure.

## Directory Structure

- `proj/src/proj/p{number}/core.clj`: Contains the Clojure solution for problem {number}
- `proj/src/proj/p{number}/p{number}.tex`: Contains the LaTeX documentation for problem {number}

## Creating a New Problem

A script is provided to help set up a new problem folder with templates:

```bash
python3 create_problem.py
```

The script will:
1. Ask for a Project Euler problem number
2. Fetch the problem description from projecteuler.net
3. Create a new folder for the problem
4. Set up a Clojure template file
5. Set up a LaTeX template file

### Requirements

The script requires the following Python packages:
- requests
- beautifulsoup4

You can install them using pip:

```bash
pip install requests beautifulsoup4
```

### Usage

1. Run the script:
   ```bash
   python3 create_problem.py
   ```

2. Enter the problem number when prompted.

3. The script will create:
   - A new folder at `proj/src/proj/p{number}/`
   - A Clojure file at `proj/src/proj/p{number}/core.clj`
   - A LaTeX file at `proj/src/proj/p{number}/p{number}.tex`

4. You can now start implementing your solution in the Clojure file and documenting it in the LaTeX file.

## Running Solutions

To run a solution, you can use the Clojure CLI or Leiningen:

```bash
# Using Clojure CLI
clj -M -m p{number}.core

# Using Leiningen
lein run -m p{number}.core
```

## Starting a REPL with a Solution

A script is provided to start a Clojure REPL with a specific problem solution loaded:

```bash
python3 start_repl.py
```

The script will:
1. Show the five most recently updated problem solutions
2. Prompt you to select one of these problems or enter a different problem number
3. Start a Clojure REPL with the selected problem's solution loaded and executed
4. Allow you to interact with the solution code in the REPL

If you select a problem that doesn't exist yet, the script will offer to create it for you using the `create_problem.py` script.

### Usage

1. Run the script:
   ```bash
   python3 start_repl.py
   ```

2. Select a problem from the list or enter a problem number.

3. The REPL will start with the problem solution loaded and executed.

4. You can now interact with the solution code in the REPL.

## Compiling LaTeX Documentation

To compile the LaTeX documentation for a problem:

```bash
cd proj/src/proj/p{number}/
pdflatex p{number}.tex
```

This will generate a PDF file with the problem statement and your solution documentation.