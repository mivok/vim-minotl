#!/usr/bin/env python
import json
import re
import sys

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

def pretty_print_outline(outline, indent = 4, curr_indent = 0):
    """Takes an internal outline data structure and prints it back out"""
    for i in outline:
        if type(i) == str:
            print "%s%s" % (curr_indent * " ", i)
        else:
            print "%s%s" % (curr_indent * " ", i[0])
            pretty_print_outline(i[1], indent, indent + curr_indent)

def print_json_outline(outline, indent = 4):
    # Prints the outline in json format
    print json.dumps(outline, indent=4)

def print_html_outline(outline, indent = 4, curr_indent = 0):
    """Prints an outline in html UL format"""
    print "%s<ul>" % (curr_indent * " ")
    for i in outline:
        if type(i) == str:
            print "%s<li>%s</li>" % (curr_indent * " ", i)
        else:
            print "%s<li>%s" % (curr_indent * " ", i[0])
            print_html_outline(i[1], indent, indent + curr_indent)
            print "%s</li>" % (curr_indent * " ")
    print "%s</ul>" % (curr_indent * " ")

def print_markdown_outline(outline, indent = 4, curr_indent = 0):
    """Prints an outline in markdown format"""
    for i in outline:
        if type(i) == str:
            print "%s* %s" % (curr_indent * " ", i)
        else:
            print "%s* %s" % (curr_indent * " ", i[0])
            print_markdown_outline(i[1], indent, indent + curr_indent)

with open(sys.argv[1]) as fh:
    lines = fh.read().split('\n')
    curr_line, outline = parse_outline(lines)
    print_markdown_outline(outline)
