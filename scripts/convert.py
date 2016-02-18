#!/usr/bin/env python
from __future__ import print_function

import json
import re
import sys
import argparse

def parse_outline(lines, curr_line = 0, curr_indent = 0):
    """Reads in an outline file and generates an internal data structure of
    the outline.

    The structure is roughly a list of lists. Each entry is a list with two
    items: a string for the parent item, and a list of child entry. If an
    entry has no children, then the entry is just a string.
    """
    outline = []
    indent_re = re.compile(r'^\s*')
    while curr_line < len(lines):
        line = lines[curr_line]
        indent = indent_re.match(line).end()
        if line.strip() == '' or line.startswith('#'):
            curr_line += 1
            continue
        line = line.lstrip()
        if indent > curr_indent:
            curr_line, children = parse_outline(lines, curr_line, indent)
            outline[-1] = [outline[-1], children]
        elif indent == curr_indent:
            outline.append(line)
            curr_line += 1
        else:
            return curr_line, outline
    return curr_line, outline

def convert_to_minotl(outline, indent = 4, curr_indent = 0):
    """Converts to a standard minotl format"""
    lines = []
    for i in outline:
        if type(i) == str:
            lines.append("%s%s" % (curr_indent * " ", i))
        else:
            lines.append("%s%s" % (curr_indent * " ", i[0]))
            lines.append(convert_to_minotl(i[1], indent, indent +
                                           curr_indent))
    return '\n'.join(lines)

def convert_to_json(outline, indent = 4):
    """Converts the outline to json"""
    return json.dumps(outline, indent=4)

def convert_to_html(outline, indent = 4, curr_indent = 0):
    """Converts the outline to html UL format"""
    lines = []
    lines.append("%s<ul>" % (curr_indent * " "))
    for i in outline:
        if type(i) == str:
            lines.append("%s<li>%s</li>" % ((curr_indent + indent)* " ", i))
        else:
            lines.append("%s<li>%s" % ((curr_indent + indent) * " ", i[0]))
            lines.append(convert_to_html(i[1], indent, indent + curr_indent))
            lines.append("%s</li>" % ((curr_indent + indent) * " "))
    lines.append("%s</ul>" % (curr_indent * " "))
    return '\n'.join(lines)

def convert_to_opml(outline, indent = 4, curr_indent = 0):
    """Converts the outline to OPML"""
    lines = []
    lines.append('<?xml version="1.0" encoding="utf-8"?>')
    lines.append('<opml version="1.0">')
    lines.append('<head><title>Outline</title></head>')
    lines.append('<body>')
    lines.append(convert_to_opml_fragment(outline, indent, curr_indent +
                                          indent))
    lines.append('</body>')
    lines.append('</opml>')
    return '\n'.join(lines)

def convert_to_opml_fragment(outline, indent = 4, curr_indent = 0):
    """Converts the outline to an OPML fragment"""
    lines = []
    for i in outline:
        if type(i) == str:
            lines.append("%s<outline text=\"%s\" />" % (curr_indent * " ", i))
        else:
            lines.append("%s<outline text=\"%s\">" % (curr_indent * " ", i[0]))
            lines.append(convert_to_opml_fragment(i[1], indent, indent + curr_indent))
            lines.append("%s</outline>" % (curr_indent * " "))
    return '\n'.join(lines)

def convert_to_markdown(outline, indent = 4, curr_indent = 0):
    """Convert an outline to markdown format"""
    lines = []
    for i in outline:
        if type(i) == str:
            lines.append("%s* %s" % (curr_indent * " ", i))
        else:
            lines.append("%s* %s" % (curr_indent * " ", i[0]))
            lines.append(convert_to_markdown(i[1], indent, indent +
                                             curr_indent))
    return '\n'.join(lines)

if __name__ == '__main__':
    formats = [i[11:] for i in locals().keys() if i.startswith('convert_to_')]
    parser = argparse.ArgumentParser(
        description='Convert a minotl outline to different formats',
        epilog="Supported formats: %s" % ' '.join(formats))
    parser.add_argument('--format', default='markdown', help='The format to convert to')
    parser.add_argument('filename', help='Path to the minotl file')
    args = parser.parse_args()


    try:
        func = locals()["convert_to_%s" % args.format]
    except KeyError:
        print("Unknown format: %s" % args.format)
        sys.exit(1)

    with open(args.filename) as fh:
        lines = fh.read().split('\n')
        _, outline = parse_outline(lines)
        converted = func(outline)
        print(converted)
