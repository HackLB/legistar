#!/usr/bin/env python
import os, sys
from pprint import pprint
import simplejson as json
import requests
from bs4 import BeautifulSoup
import feedparser
import urllib.parse
import dateparser
from sh import split
from geopy.geocoders import Nominatim, GoogleV3
from geopy.exc import GeocoderTimedOut


with open('../secrets.json') as f:    
    secrets = json.load(f)

geolocator = GoogleV3(api_key=secrets['google_api_key'])

base_url = 'http://longbeach.legistar.com/'
rss = 'http://longbeach.legistar.com/Feed.ashx?M=Calendar&ID=3681868&GUID=bdc62cd7-29c7-4595-8c96-c86429f1d954&Mode=Last%20Month&Title=City+of+Long+Beach+-+Calendar+(Last+Month)'



def geocode(address):
    try:
        location = geolocator.geocode(address, timeout=2)
        if location:
            data = {"latitude": location.latitude, "longitude": location.longitude, "address": location.address}
            print(data)
            return data
        else:
            return None
    except GeocoderTimedOut:
        return geocode(address)


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

def fix_address(address):
    if 'bay shore library' in address.lower():
        return '195 Bay Shore Avenue, Long Beach, CA'
    if 'council chamber' in address.lower():
        return '333 W. Ocean Boulevard, Long Beach, CA'
    if '333 w' in address.lower():
        return '333 W. Ocean Boulevard, Long Beach, CA'
    if 'Long Beach Yacht Club' in address:
        return '6201 Appian Way, Long Beach, CA'
    if '4801 Airport Plaza Drive' in address:
        return '4801 Airport Plaza Drive, Long Beach, CA'
    if 'Senior Center Library' in address:
        return 'El Dorado Park West Community Center, Long Beach, CA'
    if 'Code Enforcement Conference Room' in address:
        return '100 W. Broadway, Suite 400, Long Beach, CA 90802'
    if 'Neighborhood Services Bureau' in address.lower():
        return '100 W. Broadway, Suite 550, Long Beach, CA 90802'

    return '{}, Long Beach, CA'.format(address).replace('\n', ', ')


def enhance_and_clean_record(record):
    url = record['link']
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')


    # Get meeting location
    meeting_location = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblLocation'}).string
    record['location'] = meeting_location

    # Geocoding location
    if record['location']:
        cleaned_address = fix_address(record['location'])

        geocoded_location = geocode(cleaned_address)
        if geocoded_location:
            record['coordinates'] = geocoded_location
        else:
            print('record location: {}'.format(cleaned_address))
            print('location not found')


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


    # Get agenda items if existing
    record['agenda_items'] = []
    table_body = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_gridMain_ctl00'}).find('tbody')
    agenda_rows = table_body.find_all('tr')

    # If meeting record has agenda items listed
    if len(table_body.find_all('tr', {'class': 'rgNoRecords'})) == 0:
        # For each agenda item noted...
        for row in agenda_rows:
            cells = row.find_all('td')

            row_rec = {}

            # Get link for agenda item
            if len(cells[0].find_all('a')) > 0:
                row_rec['url'] = urllib.parse.urljoin(base_url, cells[0].find('a')['href'])
                row_rec['file_num'] = cells[0].find('a').string
            else:
                row_rec['url'] = None
                row_rec['file_num'] = None
            
            # Agenda item version
            try:
                row_rec['version'] = int(cells[1].string.replace('.','').strip())
            except:
                row_rec['version'] = None
            
            # Agenda item number
            try:
                row_rec['agenda_num'] = int(cells[2].string.replace('.','').strip())
            except:
                row_rec['agenda_num'] = None


            # Agenda item name, type, and title
            row_rec['name'] = cells[3].string
            row_rec['type'] = cells[4].string
            row_rec['title'] = cells[5].string


            # Get agenda item attachments if available
            r_agenda_page = requests.get(row_rec['url'])
            agenda_page = BeautifulSoup(r_agenda_page.content, 'html.parser')

            # Initialize list for attachments
            row_rec['attachments'] = []


            # Get attachment links if they exist
            if agenda_page.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblAttachments2'}) is not None:
                attachment_links = agenda_page.find('span', {'id': 'ctl00_ContentPlaceHolder1_lblAttachments2'}).find_all('a')
            else:
                attachment_links = []

            # For each attachment found, create a record for it and add to agenda record
            attachment_index = 1
            for attachment in attachment_links:
                attachment_rec = {}

                attachment_rec['num'] = attachment_index
                attachment_rec['url'] = urllib.parse.urljoin(base_url, attachment['href'])
                attachment_rec['filename'] = attachment.string.strip('.&;* #@').replace('&','-')

                row_rec['attachments'].append(attachment_rec)
                attachment_index += 1

            record['agenda_items'].append(row_rec)


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

    print('Saving record of _{}_\nlocated at: {}'.format(record['title'], record['location']))

    path = os.path.join(directory, 'data.json')
    with open(path, 'w') as f:
        json.dump(record, f, indent=4, ensure_ascii=False, sort_keys=True)

    agenda_path = os.path.join(directory, 'agenda.pdf')
    if record['agenda'] and not os.path.exists(agenda_path):
        download(record['agenda'], agenda_path)

    minutes_path = os.path.join(directory, 'minutes.pdf')
    if record['minutes'] and not os.path.exists(minutes_path):
        download(record['minutes'], minutes_path)

    for agenda_item in record['agenda_items']:
        agenda_dir_name = '{}'.format(agenda_item['agenda_num'])

        agenda_dir = os.path.join(directory, agenda_dir_name)
        os.makedirs(agenda_dir, exist_ok=True)

        # Loop through each attachment and save it
        for attachment in agenda_item['attachments']:
            attachment_path = os.path.join(agenda_dir, attachment['filename'])

            # Only download if it doesnt already exist
            if not os.path.exists(attachment_path):
                print('Downloading: {}'.format(attachment['url']))
                download(attachment['url'], attachment_path)


    return True


if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))  # Path to current directory
    data_path = os.path.join(repo_path, '_data')                # Root path for record data
    os.makedirs(data_path, exist_ok=True)

    records = get_records()                     # Get Legistar records...

    print('Saving Legistar calendar data...')
    for record in records:
        save_record(record)                     # Save the scraped records to JSON files...

