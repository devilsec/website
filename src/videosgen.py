#!/usr/bin/python3

# Videos Page Generator

# Generates an updated videos page pre-build to ensure that the videos
# page is most up to date.

__author__ = 'Prithviraj Renjella Rajendra Prasad'
__version__ = '1.0'
__copyright__ = 'Copyright (c) 2022 Prithviraj Renjella Rajendra Prasad'
__license__ = 'GNU GPL v3'

# Imports
from contextlib import closing
from glob import glob
import re
from tracemalloc import start
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

# this has a bug
def find_full_element(element_name, start_pos, last_div_pos):
    global html
    opening_element = rf'<{element_name}'
    closing_element = rf'</{element_name}>'
    next_element_pos = html.find(closing_element, last_div_pos)+len(closing_element)
    start_element_end_pos = html.find('>', start_pos)+1
    div_contents = html[start_element_end_pos:next_element_pos]
    re_div_findall = len(re.findall(opening_element, div_contents))
    re_slashdiv_findall = len(re.findall(closing_element, div_contents))
    if re_div_findall == re_slashdiv_findall:
        return next_element_pos
    else:
        return find_full_element(element_name, start_pos, next_element_pos)


def find_full_div(start_pos, last_div_pos):
    return find_full_element('div', start_pos, last_div_pos)


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

    # speakers
    # div = div.replace("[Speakers]", str(retrieve_speakers(event)))
    # tags
    # div = div.replace("[Tags]", str(retrieve_tags(video)))
    div = div.replace("{{Video URL}}", video.get("videoURL"))
    div = re.sub(r"\[Description [^\]]*\]",
                 rf"{video.get('description')}", div)
    return div


def retrieve_button_tag(button_id):
    global html
    button_start = re.search(rf"(<button[^>]*id=\"{button_id}\"[^>]*>)", html)
    if button_start is None:
        raise ValueError
    button_start_pos = html.find(button_start.group(1))
    button_end_pos = find_full_element('button', button_start_pos, button_start_pos)
    if button_end_pos is None:
        raise ValueError
    button = html[button_start_pos:button_end_pos]
    return [re.sub(r">\s*<", r"><", button), button_start_pos, button_end_pos]


def complete_button_tag(tag_name, button):
    button = button.replace("[Tags]", tag_name)
    return button

def complete_tags(video):
    tag_buttons = retrieve_button_tag('tag-buttons')
    tag_button = tag_buttons[0]
    tag_names = retrieve_tags(video)
    tags = ''
    for tag_name in tag_names:
        tags += complete_button_tag(tag_name, tag_button)
    global html
    html = html.replace(tag_button, tags)

# def complete_replace_div(videos, id, iter):
#     global html
#     og_div = retrieve_div(id)
#     completed_div = complete_div(videos[iter], og_div[0])
#     html = html.replace(og_div[0], completed_div)


# def delete_div(div_id):
#     global html
#     div = retrieve_div(div_id)
#     html = html.replace(div[0], '')


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
    return datetime.strptime(video.get('date'), format_string)


def complete_videos():
    video_div = retrieve_div("videos")[0]
    completed_divs = ''
    for video in videos_index:
        completed_divs += complete_div(video, video_div)
        complete_tags(video)
    global html
    html = html.replace(video_div, completed_divs)


def videos_generation():
    complete_videos()
    open("./dist/videos.html", "w").write(html)


if __name__ == "__main__":
    videos_generation()
