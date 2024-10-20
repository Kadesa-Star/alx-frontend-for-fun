#!/usr/bin/python3
"""
File takes two arguments
This script converts markdown into html file
"""
import sys
import os


# check the number of arguments supplied
if len(sys.argv) < 3:
    sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
    sys.exit(1)

# get input and output files from supplied arguments
markdown_file = sys.argv[1]
html_file = sys.argv[2]

# check if markdown file exists
if not os.path.isfile(markdown_file):
    sys.stderr.write(f"Missing {markdown_file}\n")
    sys.exit(1)

# if all is fine exit with 0 (success)
sys.exit(0)
