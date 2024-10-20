#!/usr/bin/env python3

import sys
import re
import hashlib

def md5_hash(text):
    """Returns the MD5 hash of the input text in lowercase."""
    return hashlib.md5(text.encode()).hexdigest()

def markdown_to_html(markdown):
    html_lines = []
    inside_list = False
    inside_paragraph = False
    
    for line in markdown.splitlines():
        line = line.rstrip()  # Remove trailing whitespace

        # Handling headers
        if line.startswith('#'):
            level = line.count('#')
            html_lines.append(f"<h{level}>{line[level:].strip()}</h{level}>")
            inside_paragraph = False
            continue
        
        # Handling lists
        if line.startswith('- '):
            if not inside_list:
                html_lines.append("<ul>")
                inside_list = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
            inside_paragraph = False
            continue
        elif inside_list:
            html_lines.append("</ul>")
            inside_list = False
        
        # Handling paragraphs
        if line == '':
            if inside_paragraph:
                html_lines.append("</p>")
                inside_paragraph = False
            continue
        
        # Start a new paragraph
        if not inside_paragraph:
            html_lines.append("<p>")
            inside_paragraph = True

        # Process bold and italics
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)  # Bold syntax
        line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)  # Italics syntax
        
        # Process [[Hello]] for MD5 conversion
        line = re.sub(r'\[\[(.*?)\]\]', lambda m: md5_hash(m.group(1)), line)

        # Process ((Hello Chicago)) for removing 'c' characters
        line = re.sub(r'\(\((.*?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)
        
        # Add line with breaks for multi-line paragraphs
        html_lines.append(line)
    
    # Close any open tags
    if inside_paragraph:
        html_lines.append("</p>")
    if inside_list:
        html_lines.append("</ul>")
    
    return "\n".join(html_lines)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: markdown2html.py <input_markdown_file> <output_html_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        markdown_content = f.read()

    html_content = markdown_to_html(markdown_content)

    with open(output_file, 'w') as f:
        f.write(html_content)
