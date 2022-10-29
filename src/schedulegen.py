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


# Retrieve Schedule HTML Page:

html = open("./dist/schedule.html", "r").read()


# HTML Component Functions:


def find_full_div(start_pos, last_div_pos):
    global html
    next_div_pos = html.find('</div>', last_div_pos)+6
    start_div_end_pos = html.find('>', start_pos)+1
    div_contents = html[start_div_end_pos:next_div_pos]
    if len(re.findall(r"<div",
                      div_contents)) == len(re.findall(r"</div>",
                                                       div_contents)):
        return next_div_pos
    else:
        find_full_div(start_pos, next_div_pos)


def retrieve_div(div_id):
    global html
    div_start = re.search(rf"(<div[^>]*id=\"{div_id}\"[^>]*>)", html)
    if div_start is None:
        raise ValueError
    div_start_pos = html.find(div_start.group(1))
    div_end_pos = find_full_div(div_start_pos, div_start_pos)
    if div_end_pos is None:
        raise ValueError
    div = html[div_start_pos:div_end_pos]
    return [re.sub(r">\s*<", r"><", div), div_start_pos, div_end_pos]


def complete_div(event, div):
    # Parse Data
    div = div.replace("[Name]", event.get("name"))
    parsed_date = parse_date(event)
    if parsed_date.strftime("%z") == '-0700':
        div = div.replace("[Date]", parsed_date.strftime("%d %b %Y MST"))
        div = div.replace("[Time]", parsed_date.strftime("%H:%M MST"))
    else:
        div = div.replace("[Date]", parsed_date.strftime("%d %b %Y UTC%z"))
        div = div.replace("[Time]", parsed_date.strftime("%H:%M UTC%z"))
    div = div.replace("[Duration]", event.get("duration"))
    div = div.replace("[Location]", event.get("location"))
    div = div.replace("{{ Location URL }}", event.get("locationURL"))
    div = re.sub(r"\[Description [^\]]*\]",
                 rf"{event.get('description')}", div)
    div = div.replace("{{ ICS URL }}", event.get("icsURL"))
    div = div.replace("[Speakers]", str(retrieve_speakers(event)))
    return div


def complete_replace_div(events, id, iter):
    global html
    og_div = retrieve_div(id)
    completed_div = complete_div(events[iter], og_div[0])
    html = html.replace(og_div[0], completed_div)


def delete_div(div_id):
    global html
    div = retrieve_div(div_id)
    html = html.replace(div[0], '')


def complete_upcoming(events):
    if len(events) < 4:
        for i in range(4):
            if i+1 >= len(events):
                delete_div(f"upcoming-{i}")
            else:
                complete_replace_div(events, f"upcoming-{i}", i)
    else:
        for i in range(4):
            complete_replace_div(events, f"upcoming-{i}", i)


def complete_category(category):
    id = category.get('id')
    events = []
    for e in event_index:
        if e.get('category') == id:
            events.append(e)
    category_div = retrieve_div(f"category-{id}")[0]
    completed_divs = ''
    for e in events:
        completed_divs += complete_div(e, category_div)
    global html
    html = html.replace(category_div, completed_divs)


def complete_event_categories():
    for c in category_index:
        complete_category(c)


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


def schedule_generation():
    complete_upcoming(event_index)
    complete_event_categories()
    open("./dist/schedule.html", "w").write(html)


def home_generation():
    index_html = open("./dist/index.html", "r").read()
    event = event_index[0]
    date = parse_date(event)
    index_html = index_html.replace("[TITLE]", event.get('name'))
    index_html = index_html.replace("[DATE]", date.strftime("%d %b %Y"))
    index_html = index_html.replace("[TIME]", date.strftime("%H:%M"))
    index_html = index_html.replace("[DURATION]", event.get('duration'))
    index_html = index_html.replace("[LOCATION]", event.get('location'))
    open("./dist/index.html", "w").write(index_html)


if __name__ == "__main__":
    home_generation()
    schedule_generation()
