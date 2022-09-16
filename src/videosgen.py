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
    return json.loads(requests.get(f"https://raw.githubusercontent.com/devilsec/events-index/master/{name}.json").text)


videos_index = retrieve_index_json('videos').get('videos')
tags_index = retrieve_index_json('tags').get('tags')

# Retrieve Videos HTML Page:

html = open("./dist/videos.html", "r").read()


