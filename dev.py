#!/usr/bin/env python
import os, sys
from pprint import pprint
import simplejson as json
import hashlib


# url = 'https://wwwbitprod1.longbeach.gov/GarageSalePermit/SearchByDate.aspx'
rss = 'http://longbeach.legistar.com/Feed.ashx?M=Calendar&ID=3443504&GUID=0fe979a8-f2da-4787-a541-6ccef967561e&Mode=This%20Year&Title=City+of+Long+Beach+-+Calendar+(This+Year)'


def getmd5(message):    
    """
    Returns MD5 hash of string passed to it.
    """
    return hashlib.md5(message.encode('utf-8')).hexdigest()


def scrape_records():
    """
    Extracts garage sale records from the city garage sale Web page,
    then puts each record into a dictionary and returns a list of dictionaries.
    """
    print('Getting garage sales data...')
    
    records = None
    return records


def get_subdirectory(base_name):
    """
    Takes the base filename and returns a path to a subdirectory, creating it if needed.
    """
    sub_dir = os.path.join(data_path, base_name[-8:-6], base_name[-6:-4], base_name[-4:-2])
    os.makedirs(sub_dir, exist_ok=True)
    return sub_dir


def save_records(records):
    """
    Saves records to invidual JSON files.
    Records are per-address. Each new garage sale for 
    a given address gets appended to its existing file.
    Files are named and organized based on an MD5 of 
    the address.
    """
    print('Saving garage sales data...')
    for record in records:
        print('Do something')



if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))  # Path to current directory
    data_path = os.path.join(repo_path, '_data')                # Root path for record data
    os.makedirs(data_path, exist_ok=True)

    records = scrape_records()                  # Scrape Legistar records...
    save_records(records)                       # Save the scraped records to JSON files...

