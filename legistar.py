#!/usr/bin/env python
import os, sys
from pprint import pprint
import simplejson as json
import requests
from bs4 import BeautifulSoup
import feedparser
import urllib.parse
import dateparser


base_url = 'http://longbeach.legistar.com/'
rss = 'http://longbeach.legistar.com/Feed.ashx?M=Calendar&ID=3443504&GUID=0fe979a8-f2da-4787-a541-6ccef967561e&Mode=This%20Year&Title=City+of+Long+Beach+-+Calendar+(This+Year)'


def get_records():
    """
    Extracts city meeting records from the Legistar calendar
    RSS feed, then puts each record into a dictionary and returns a list of dictionaries.
    """
    print('Getting Legistar calendar data...')
    data = feedparser.parse(rss)
    print('Got {} items'.format(len(data.entries)))
    return data.entries


def enhance_and_clean_record(record):
    url = record['link']
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')


    # Get meeting name
    meeting_name = soup.find('a', {'id': 'ctl00_ContentPlaceHolder1_hypName'}).string
    record['name'] = meeting_name


    # Get agenda if existing
    agenda_ele = soup.find('a', {'id': 'ctl00_ContentPlaceHolder1_hypAgenda'})
    agenda = None
    if agenda_ele:
        try:
            agenda = urllib.parse.urljoin(base_url, agenda_ele['href'])
        except KeyError:
            pass
    record['agenda'] = agenda


    # Get minutes if existing
    minutes_ele = soup.find('a', {'id': 'ctl00_ContentPlaceHolder1_hypMinutes'})
    minutes = None
    if minutes_ele:
        try:
            minutes = urllib.parse.urljoin(base_url, minutes_ele['href'])
        except KeyError:
            pass
    record['minutes'] = minutes

    del(record['published'])
    del(record['published_parsed'])
    del(record['links'])
    del(record['guidislink'])
    del(record['tags'])
    del(record['title_detail'])
    del(record['summary_detail'])

    dt_string = (' ').join(record['title'].split(' - ')[1:3])
    record['datetime'] = dateparser.parse(dt_string).isoformat()

    return record



def get_subdirectory(record):
    """
    Takes the base filename and returns a path to a subdirectory, creating it if needed.
    """

    cleaned_meeting_name = record['name'].lower().replace(' ', '_').replace(',', '').replace('\'', '').replace('(', '').replace(')', '')

    meeting_dir = record['datetime'].replace(':','.')

    sub_dir = os.path.join(data_path, cleaned_meeting_name, meeting_dir)
    os.makedirs(sub_dir, exist_ok=True)
    return sub_dir



def save_record(record):
    record = enhance_and_clean_record(record)
    directory = get_subdirectory(record)

    path = os.path.join(directory, 'data.json')
    with open(path, 'w') as f:
        json.dump(record, f, indent=4, ensure_ascii=False, sort_keys=True)

    agenda_path = os.path.join(directory, 'agenda.pdf')
    if record['agenda'] and not os.path.exists(agenda_path):
        r = requests.get(record['agenda'])
        with open(agenda_path, 'wb') as f:
            f.write(r.content)

    minutes_path = os.path.join(directory, 'minutes.pdf')
    if record['minutes'] and not os.path.exists(minutes_path):
        r = requests.get(record['minutes'])
        with open(minutes_path, 'wb') as f:
            f.write(r.content)



if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))  # Path to current directory
    data_path = os.path.join(repo_path, '_data')                # Root path for record data
    os.makedirs(data_path, exist_ok=True)

    records = get_records()                     # Get Legistar records...

    print('Saving Legistar calendar data...')
    for record in records:
        save_record(record)                     # Save the scraped records to JSON files...

