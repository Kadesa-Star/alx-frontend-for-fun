#!/usr/bin/python3
"""
Markdown script using Python to convert Markdown to HTML.
"""
import sys
import os.path
import re
import hashlib


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        exit(1)

    if not os.path.isfile(sys.argv[1]):
        print('Missing {}'.format(sys.argv[1]), file=sys.stderr)
        exit(1)

    with open(sys.argv[1]) as read:
        with open(sys.argv[2], 'w') as html:
            unordered_start, ordered_start, paragraph = False, False, False

            """ Loop through each line of the input Markdown file. """
            for line in read:
                """ Replace bold and italic Markdown syntax with HTML. """
                line = line.replace('**', '<b>', 1)
                line = line.replace('**', '</b>', 1)
                line = line.replace('__', '<em>', 1)
                line = line.replace('__', '</em>', 1)

                """ Find and replace [[text]] with its MD5 hash. """
                md5 = re.findall(r'\[\[.+?\]\]', line)
                md5_inside = re.findall(r'\[\[(.+?)\]\]', line)
                if md5:
                    line = line.replace(md5[0], hashlib.md5(
                        md5_inside[0].encode()).hexdigest())

                """ Remove all 'c' characters from ((text)). """
                remove_letter_c = re.findall(r'\(\(.+?\)\)', line)
                remove_c_more = re.findall(r'\(\((.+?)\)\)', line)
                if remove_letter_c:
                    remove_c_more = ''.join(
                        c for c in remove_c_more[0] if c not in 'Cc')
                    line = line.replace(remove_letter_c[0], remove_c_more)

                length = len(line)  # Length of the current line.
                headings = line.lstrip('#')  # Remove leading '#' for headers.
                heading_num = length - len(headings)  # Count header level.
                unordered = line.lstrip('-')  # Remove leading '-' for lists.
                unordered_num = length - len(unordered)  # unordered items.
                ordered = line.lstrip('*')  # Remove leading '*' for lists.
                ordered_num = length - len(ordered)  # Count ordered items.

                """ Check for headers, unordered and ordered lists. """
                if 1 <= heading_num <= 6:
                    line = '<h{}>'.format(
                        heading_num) + headings.strip() + '</h{}>\n'.format(
                        heading_num)

                """ Handle unordered list items. """
                if unordered_num:
                    if not unordered_start:
                        html.write('<ul>\n')  # Start unordered list.
                        unordered_start = True
                    line = '<li>' + unordered.strip() + '</li>\n'
                if unordered_start and not unordered_num:
                    html.write('</ul>\n')  # End unordered list.
                    unordered_start = False

                """ Handle ordered list items. """
                if ordered_num:
                    if not ordered_start:
                        html.write('<ol>\n')  # Start ordered list.
                        ordered_start = True
                    line = '<li>' + ordered.strip() + '</li>\n'
                if ordered_start and not ordered_num:
                    html.write('</ol>\n')  # End ordered list.
                    ordered_start = False

                """ Handle paragraphs and line breaks. """
                if not (heading_num or unordered_start or ordered_start):
                    if not paragraph and length > 1:
                        html.write('<p>\n')  # Start new paragraph.
                        paragraph = True
                    elif length > 1:
                        html.write('<br/>\n')  # Add line break.
                    elif paragraph:
                        html.write('</p>\n')  # End current paragraph.
                        paragraph = False

                """ Write the processed line to the HTML output. """
                if length > 1:
                    html.write(line)

            """ Close any open lists or paragraphs at the end. """
            if unordered_start:
                html.write('</ul>\n')
            if ordered_start:
                html.write('</ol>\n')
            if paragraph:
                html.write('</p>\n')
    exit(0)
