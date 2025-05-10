#!/usr/bin/env python3
"""
Unit tests for the start_repl.py script.
"""

import unittest
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock
import importlib.util

# Import the start_repl module
script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start_repl.py")
spec = importlib.util.spec_from_file_location("start_repl", script_path)
start_repl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(start_repl)

class TestStartRepl(unittest.TestCase):
    """Test cases for the start_repl.py script."""
    
    def test_extract_problem_number(self):
        """Test extracting problem numbers from directory names."""
        self.assertEqual(start_repl.extract_problem_number("p123"), 123)
        self.assertEqual(start_repl.extract_problem_number("p1"), 1)
        self.assertIsNone(start_repl.extract_problem_number("not_a_problem"))
        self.assertIsNone(start_repl.extract_problem_number(""))
    
    @patch('os.listdir')
    @patch('os.path.isdir')
    def test_get_problem_directories(self, mock_isdir, mock_listdir):
        """Test getting problem directories."""
        mock_listdir.return_value = ['p1', 'p2', 'not_a_problem', 'p123', '.hidden']
        mock_isdir.side_effect = lambda path: os.path.basename(path) in ['p1', 'p2', 'not_a_problem', 'p123']
        
        problem_dirs = start_repl.get_problem_directories()
        self.assertEqual(set(problem_dirs), {'p1', 'p2', 'p123'})
    
    @patch('start_repl.get_problem_directories')
    @patch('os.path.exists')
    @patch('os.path.getmtime')
    def test_get_recent_problems(self, mock_getmtime, mock_exists, mock_get_dirs):
        """Test getting recent problems."""
        mock_get_dirs.return_value = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6']
        mock_exists.return_value = True
        
        # Set modification times (newer to older)
        mock_getmtime.side_effect = lambda path: {
            'p3': 1000,
            'p1': 900,
            'p6': 800,
            'p2': 700,
            'p5': 600,
            'p4': 500
        }[os.path.basename(os.path.dirname(path))]
        
        recent = start_repl.get_recent_problems(limit=3)
        self.assertEqual(len(recent), 3)
        
        # Check that problems are sorted by modification time (newest first)
        problem_dirs = [item[0] for item in recent]
        self.assertEqual(problem_dirs, ['p3', 'p1', 'p6'])
    
    @patch('subprocess.run')
    @patch('os.chdir')
    def test_start_repl_with_problem(self, mock_chdir, mock_run):
        """Test starting REPL with a problem."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Patch the project directory to use the temporary directory
            with patch('os.path.dirname', return_value=tmpdir):
                # Create a mock project directory
                os.makedirs(os.path.join(tmpdir, "proj"), exist_ok=True)
                
                # Call the function
                start_repl.start_repl_with_problem(42)
                
                # Check that subprocess.run was called with the correct arguments
                mock_run.assert_called_once()
                args = mock_run.call_args[0][0]
                self.assertEqual(args[0], "lein")
                self.assertEqual(args[1], "repl")
                self.assertEqual(args[2], ":init")
                
                # Check that the init file was created and contains the problem number
                init_file = args[3]
                self.assertTrue(os.path.exists(init_file))
                with open(init_file, 'r') as f:
                    content = f.read()
                    self.assertIn("p42", content)
                    self.assertIn("Problem 42", content)

if __name__ == '__main__':
    unittest.main()