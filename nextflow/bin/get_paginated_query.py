#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get the results from each page of the API query results

$ bin/get_paginated_query.py "https://silo:6886/api/v1/files/?sample__type=N&limit=1000" <token> path
"""
import sys
import ssl
import json
from urllib.request import Request, urlopen # use this because `requests` is not installed by default
from urllib.parse import urlparse, urlunparse

args = sys.argv[1:]
start_url = args[0]
token = args[1]
res_key = args[2]
headers = {'Authorization': 'Token ' + token}

# do not check SSL cert because its self signed
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def build_url(next_url, base_url = start_url):
    """
    The API returns the wrong URL in the 'next' field in the response so need to use the original URL to
    rebuild the correct one
    """
    base_parts = urlparse(base_url)
    next_parts = urlparse(next_url)
    parts = [base_parts.scheme, base_parts.netloc, next_parts.path, next_parts.params, next_parts.query, next_parts.fragment]
    url = urlunparse(parts)
    return(url)

def get_page(url, headers = headers, context=ctx):
    """make GET request to the URL and return the result"""
    req = Request(url, headers = headers)
    with urlopen(req, context=context) as response:
        the_page = response.read()
        try:
            data = json.loads(the_page)
        except TypeError: # the JSON object must be str, not 'bytes'
            data = json.loads(the_page.decode('utf-8'))
    return(data)

# loop over all the pages and print each 'results' item from each page for the desire key value
query_url = start_url
while True:
    data = get_page(url = query_url)
    for item in data['results']:
        print(item[res_key])
    next_url = data['next']
    if next_url is not None:
        query_url = build_url(next_url)
    else:
        break
