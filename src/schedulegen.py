#!/usr/bin/python3

# Schedule Page Generator

# Generates an updated schedule page pre-build to ensure that the schedule
# page is most up to date.

__author__ = 'Daylam Tayari'
__version__ = '1.0'
__copyright__ = 'Copyright (c) 2022 Daylam Tayari'
__license__ = 'GNU GPL v3'


# Imports
import re


# HTML Component Functions:


def find_full_div(html, start_pos, last_div_pos):
    next_div_pos = html.find('</div>', last_div_pos)
    start_div_end_pos = html.find('>', start_pos)
    print(next_div_pos)
    print(start_div_end_pos)
    div_contents = html[start_div_end_pos:next_div_pos]
    print(len(re.findall(r"<div", div_contents)))
    print(len(re.findall(r"</div>", div_contents)))
    print(div_contents)
    if len(re.findall(r"<div", div_contents)) == len(re.findall(r"</div>", div_contents)):
        return next_div_pos
    else:
        print(True)
        find_full_div(html, start_pos, next_div_pos)


def retrieve_div(html, div_id):
    html = html
    div_id = div_id
    div_start = re.search(rf"(<div.*id=\"{div_id}\".*>)", html, re.IGNORECASE)
    if div_start is None:
        raise ValueError
    div_start_pos = div_start.start(1)
    div_end_pos = find_full_div(html, div_start_pos, div_start_pos)
    if div_end_pos is None:
        raise ValueError
    return html[div_start_pos:div_end_pos+5]
