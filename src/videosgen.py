#!/usr/bin/python3

# Videos Page Generator

# Generates an updated videos page pre-build to ensure that the videos
# page is most up to date.

__author__ = 'Prithviraj Renjella Rajendra Prasad'
__version__ = '1.0'
__copyright__ = 'Copyright (c) 2022 Prithviraj Renjella Rajendra Prasad'
__license__ = 'GNU GPL v3'

# Imports
import re
import requests
import json
from datetime import datetime

# Retrieve Indexes as Parsed JSON:

def retrieve_index_json(name):
    return json.loads(requests.get(f"https://raw.githubusercontent.com/devilsec/videos-index/master/{name}.json").text)


videos_index = retrieve_index_json('videos').get('videos')
tags_index = retrieve_index_json('tags').get('tags')

# Retrieve Videos HTML Page:

html = open("./dist/videos.html", "r").read()

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

def complete_div(video, div):
    # Parse Data
    div = div.replace("[Title]", video.get("title"))
    div = div.replace("[Date]", parse_date(video).strftime("%d %b %Y"))
    # div = div.replace("[Duration]", event.get("duration"))
    # div = div.replace("[Location]", event.get("location"))
    # div = div.replace("{{ Location URL }}", event.get("locationURL"))
    # div = re.sub(r"\[Description [^\]]*\]",
    #              rf"{event.get('description')}", div)
    # div = div.replace("{{ ICS URL }}", event.get("icsURL"))

    #speakers
    # div = div.replace("[Speakers]", str(retrieve_speakers(event)))
    #tags
    div = div.replace("[Tags]", str(retrieve_tags(video)))
    div = div.replace("{{Video URL}}", video.get("videoURL"))
    div = re.sub(r"\[Description [^\]]*\]",
                 rf"{video.get('description')}", div)
    return div

def complete_replace_div(videos, id, iter):
    global html
    og_div = retrieve_div(id)
    completed_div = complete_div(videos[iter], og_div[0])
    html = html.replace(og_div[0], completed_div)

def delete_div(div_id):
    global html
    div = retrieve_div(div_id)
    html = html.replace(div[0], '')




def retrieve_tags(video):
    tag_names_array = []
    tags = video.get('tags')
    for tag in tags:
        if tags_index[tag].get('id') == tag:
            tag_names_array.append(f"{tags_index[tag].get('name')}")
        else:
            for i in tags_index:
                if i.get('id') == tag:
                    tag_names_array.append(f"{i.get('name')}")
                    break
    return tag_names_array

# Returns an array containing the date and time with timezone
def parse_date(video):
    format_string = '%Y-%m-%d'
    # iso_date = event.get('date')
        # iso_date = event
    # timestamp = re.match(
    #     r"^(\-\-|[0-9]{4}[\-]?)([0-1][0-9])[\-]?[0-3][0-9]$", iso_date)
    # if timestamp is None:
    #     raise ValueError(
    #         f"Date value for event with ID {event.get('id')} is in an invalid format.")
    # if timestamp.group(3) is not None:
    #     format_string += ':%M'
    # if timestamp.group(4) is not None:
    #     format_string += ':%S'
    # if timestamp.group(5) is not None:
    #     format_string += ':%f'
    # if timestamp.group(6) is None:
    #     iso_date += '+00:00'
    return datetime.strptime(video, format_string)