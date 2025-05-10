#!/usr/bin/env python3
"""
Test script for create_problem.py
This script tests the HTML to LaTeX conversion functionality.
"""

import unittest
from create_problem import html_to_latex

class TestHtmlToLatex(unittest.TestCase):
    """Test cases for the html_to_latex function."""
    
    def test_basic_formatting(self):
        """Test basic HTML formatting conversion."""
        html = """<div class="problem_content">
        <p>This is a <strong>bold</strong> and <em>italic</em> text.</p>
        </div>"""
        
        latex = html_to_latex(html)
        
        # Check if bold and italic formatting is converted correctly
        self.assertIn("\\textbf{bold}", latex)
        self.assertIn("\\textit{italic}", latex)
    
    def test_lists(self):
        """Test HTML list conversion."""
        html = """<div class="problem_content">
        <p>Here's a list:</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        <p>And an ordered list:</p>
        <ol>
            <li>First</li>
            <li>Second</li>
        </ol>
        </div>"""
        
        latex = html_to_latex(html)
        
        # Check if lists are converted correctly
        self.assertIn("\\begin{itemize}", latex)
        self.assertIn("\\item Item 1", latex)
        self.assertIn("\\begin{enumerate}", latex)
        self.assertIn("\\item First", latex)
    
    def test_special_characters(self):
        """Test special character handling."""
        html = """<div class="problem_content">
        <p>Special characters: & % $ # _ { } ~ ^ \\</p>
        </div>"""
        
        latex = html_to_latex(html)
        
        # Check if special characters are escaped
        for char in ['&', '%', '$', '#', '_', '{', '}', '~', '^', '\\']:
            self.assertIn(f"\\{char}", latex)
    
    def test_html_entities(self):
        """Test HTML entity conversion."""
        html = """<div class="problem_content">
        <p>HTML entities: &lt;code&gt; and &gt;value&lt;</p>
        </div>"""
        
        latex = html_to_latex(html)
        
        # Check if HTML entities are converted and then escaped
        self.assertIn("\\<code\\>", latex)
        self.assertIn("\\>value\\<", latex)
    
    def test_tables(self):
        """Test table conversion."""
        html = """<div class="problem_content">
        <table>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
            </tr>
            <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
            </tr>
        </table>
        </div>"""
        
        latex = html_to_latex(html)
        
        # Check if table is converted correctly
        self.assertIn("\\begin{tabular}", latex)
        self.assertIn("Header 1 & Header 2", latex)
        self.assertIn("Cell 1 & Cell 2", latex)
    
    def test_newline_cleanup(self):
        """Test newline cleanup."""
        html = """<div class="problem_content">
        <p>Paragraph 1</p>
        
        
        
        <p>Paragraph 2</p>
        </div>"""
        
        latex = html_to_latex(html)
        
        # Check if excessive newlines are cleaned up
        self.assertNotIn("\n\n\n", latex)
    
    def test_math_content(self):
        """Test math content handling."""
        html = """<div class="problem_content">
        <p>Math: <span class="math">x^2 + y^2 = z^2</span></p>
        </div>"""
        
        latex = html_to_latex(html)
        
        # Check if math content is preserved
        self.assertIn("$x^2 + y^2 = z^2$", latex)

if __name__ == "__main__":
    unittest.main()