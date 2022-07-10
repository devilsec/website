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
import requests
import json
from datetime import datetime


# Retrieve Indexes as Parsed JSON:

def retrieve_index_json(name):
    return json.loads(requests.get(f"https://raw.githubusercontent.com/devilsec/events-index/master/{name}.json").text)


event_index = retrieve_index_json('events').get('events')
speaker_index = retrieve_index_json('speakers').get('speakers')
category_index = retrieve_index_json('categories').get('categories')


# HTML Component Functions:


def find_full_div(html, start_pos, last_div_pos):
    next_div_pos = html.find('</div>', last_div_pos)
    start_div_end_pos = html.find('>', start_pos)
    div_contents = html[start_div_end_pos:next_div_pos]
    if len(re.findall(r"<div",
                      div_contents)) == len(re.findall(r"</div>",
                                                       div_contents)):
        return next_div_pos
    else:
        print(True)
        find_full_div(html, start_pos, next_div_pos)


def retrieve_div(html, div_id):
    html = html
    div_id = div_id
    div_start = re.search(rf"(<div.*id=\"{div_id}\".*>)", html)
    if div_start is None:
        raise ValueError
    div_start_pos = div_start.start(1)
    div_end_pos = find_full_div(html, div_start_pos, div_start_pos)
    if div_end_pos is None:
        raise ValueError
    div = html[div_start_pos:div_end_pos + 6]
    return re.sub(r">\s*<", r"><", div)


def complete_div(event, div):
    # Parse Data
    div.replace('[Name]', event.get('name'))
    parsed_date = parse_date(event)
    div.replace('[Date]', parsed_date.strftime('%d %b %Y UTC%z'))
    div.replace('[Time]', parsed_date.strftime('%H:%m UTC%z'))
    div.replace('[Duration]', event.get('duration'))
    div.replace('[Location]', event.get('location'))
    div.replace('{{ Location URL }}', event.get('locationURL'))
    re.sub(r"[Description [A-Za-z \.]*]", rf"{event.get('description')}", div)
    div.replace('{{ ICS URL }}', event.get('icsURL'))
    div.replace('[Speakers]', retrieve_speakers(event))
    return div


# Miscellaneous Functions


# Retrieves speaker names
def retrieve_speakers(event):
    speaker_name_array = []
    speakers = event.get('speakers')
    for s in speakers:
        if speaker_index[s].get('id') == s:
            speaker_name_array.append(f"{speaker_index[s].get('name')}")
        else:
            for i in speaker_index:
                if i.get('id') == s:
                    speaker_name_array.append(f"{i.get('name')}")
                    break
    return speaker_name_array


# Returns an array containing the date and time with timezone
def parse_date(event):
    format_string = '%Y-%m-%dT%H'
    iso_date = event.get('date')
    timestamp = re.match(
        r"^(\-\-|[0-9]{4}[\-]?)([0-1][0-9])[\-]?[0-3][0-9]T[0-2][0-9](:[0-6][0-9])?(:[0-6][0-9])?(:[0-9]{2})?([+-][0-2][0-9](:[0-6][0-9])?)?$", iso_date)
    if timestamp is None:
        raise ValueError(
            f"Date value for event with ID {event.get('id')} is in an invalid format.")
    if timestamp.group(3) is not None:
        format_string += ':%M'
    if timestamp.group(4) is not None:
        format_string += ':%S'
    if timestamp.group(5) is not None:
        format_string += ':%f'
    if timestamp.group(6) is None:
        iso_date += '+00:00'
    return datetime.strptime(iso_date, format_string+'%z')
