#!/usr/bin/env python
import os, sys, re
from pprint import pprint
import simplejson as json
import requests
from bs4 import BeautifulSoup
import feedparser
from urllib.parse import urlparse
import dateparser
from sh import split
from geopy.geocoders import Nominatim, GoogleV3
from geopy.exc import GeocoderTimedOut


"""
https://medium.com/@hoppy/how-to-test-or-scrape-javascript-rendered-websites-with-python-selenium-a-beginner-step-by-c137892216aa#.2ugnsncv4
"""


base_url = 'http://longbeach.legistar.com/'
rss = 'http://longbeach.legistar.com/Feed.ashx?M=Calendar&ID=3683065&GUID=726ec273-3eb0-48f3-94f8-d2948459d6dc&Mode=Last%20Month&Title=City+of+Long+Beach+-+Calendar+(This+Year)'



def download(url, path):
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    if os.path.getsize(path) > 1024 * 1024 * 40:  # If files are bigger than 40MB, split em up!
        split("-b", "10m", path, '{}_'.format(path))
        # os.remove(path)
        with open(path, 'w'):
            pass # Delete contents of path, but leave empty file as a marker.

    return True


def get_records():
    """
    Extracts city meeting records from the Legistar calendar
    RSS feed, then puts each record into a dictionary and returns a list of dictionaries.
    """
    print('Getting Legistar calendar data...')
    data = feedparser.parse(rss)
    print('Got {} items'.format(len(data.entries)))
    return data.entries


def get_subdirectory(record):
    """
    Takes the base filename and returns a path to a subdirectory, creating it if needed.
    """

    cleaned_meeting_name = record['name'].lower().replace(' ', '_').replace(',', '').replace('\'', '').replace('(', '').replace(')', '')

    meeting_dir = record['datetime'].replace(':','.')

    sub_dir = os.path.join(video_path, cleaned_meeting_name, meeting_dir)
    os.makedirs(sub_dir, exist_ok=True)
    return sub_dir


def get_video_page_from(page):
    print('getting video page from {}'.format(page))
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'html.parser')

    # # Get meeting location
    video_link = soup.find('a', {'class': 'videolink'})
    if video_link.string == 'Video':
        url_stub = video_link['onclick'].strip('window.open(\'').strip('\',\'video\');return false;')
        url = 'http://longbeach.legistar.com/{}'.format(url_stub)
    else:
        url = None

    return url


def get_video_url_from(page):
    print('getting video url from {}'.format(page))
    r = requests.get(page)
    # soup = BeautifulSoup(r.content, 'html.parser')
    # print(r.content)

    match = re.search('longbeach_(.+?)mp4', str(r.content))
    if match:
        return 'http://media-10.granicus.com:443/OnDemand/longbeach/{}'.format(match.group(0))
    else:
        return None


def enhance_and_clean_record(record):
    url = record['link']
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')


    # Get meeting location
    meeting_location = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblLocation'}).string
    record['location'] = meeting_location


    # Get meeting name
    meeting_name = soup.find('a', {'id': 'ctl00_ContentPlaceHolder1_hypName'}).string
    record['name'] = meeting_name

    # Cleanup record by deleting some unnecessary fields.
    # Most are specific to the original ATOM feed and not relevant
    del(record['published'])
    del(record['published_parsed'])
    del(record['links'])
    del(record['guidislink'])
    del(record['tags'])
    del(record['title_detail'])
    del(record['summary_detail'])

    # Parse meeting datetime from title
    dt_string = (' ').join(record['title'].split(' - ')[1:3])
    record['datetime'] = dateparser.parse(dt_string).isoformat()

    return record


def save_record(record):
    record = enhance_and_clean_record(record)

    # directory = get_subdirectory(record)
    directory = video_path

    video_page_url = get_video_page_from(record['link'])
    if video_page_url:
        video_url = get_video_url_from(video_page_url)
        if video_url:
            record['video_url'] = video_url
            record['video_name'] = os.path.basename(urlparse(record['video_url']).path)

            print('Saving record of *{}*\nlocated at: {}'.format(record['title'], record['location']))

            path = os.path.join(directory, '{}.json'.format(record['video_name']))
            with open(path, 'w') as f:
                json.dump(record, f, indent=4, ensure_ascii=False, sort_keys=True)

            return True
    return False


if __name__ == "__main__":
    repo_path  = os.path.dirname(os.path.realpath(sys.argv[0]))  # Path to current directory
    data_path  = os.path.join(repo_path, '_data')                # Root path for record data
    video_path = os.path.join(repo_path, '_video')                # Root path for record data
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(video_path, exist_ok=True)

    records = get_records()

    print('Saving Legistar video data...')
    for record in records:
        save_record(record)
