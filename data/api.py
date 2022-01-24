#-*-coding: utf-8-*-
"""API connection and storing functions.
"""

from datetime import MAXYEAR
import os
import pandas as pd
import requests


# api path
URL_BASE = 'https://de.openparliament.tv/api/v1/search/media/'
# maximum amount of pages per year
MAX_PAGES = 1000
CURRENT_YEAR = 2021


def get_pages(n_pages=50):
    """Get new data pages (specified amount).
    """
    # file for storing "cursor" position
    file_path = os.path.join(os.path.dirname(__file__), 'state.txt')
    try:
        # check wether we can start from where it left off
        with open(file_path, 'r', encoding='utf-8') as f:
            pass
    except:
        # if first call, start from initial data
        year = 2017
        page = 1
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f'{year};{page}')
        with open(os.path.join(os.path.dirname(__file__), 'data.csv'), 'w', encoding='utf-8') as f:
            f.write('id;;;date;;;party;;;text\n')
    # next page
    # get one page at a time (10 speeches)
    for _ in range(n_pages):
        with open(file_path, 'r', encoding='utf-8') as f:
            year, page = f.read().split(';')
            year = int(year)
            page = int(page)
        #get the year of the newest speech
        data_year = get_data({'dateFrom': f'{year}-01-01', 'page': page})
        data_year = int(data_year)
        # store states
        if data_year == year + 1 or page > MAX_PAGES:
            if year + 1 > CURRENT_YEAR:
                return
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f'{year + 1};{1}')
        else:
            page += 1
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f'{year};{page}')


def get_data(options):
    json_data = send_request(options)
    if json_data['meta']['results']['count']:
        data_year = extract_data_from_json(json_data)
    return data_year

def send_request(options):
    url = f'{URL_BASE}?{"&".join([f"{k}={v}" for k, v in options.items()])}'
    return requests.get(url).json()


def extract_data_from_json(json_data):
    data = json_data['data']
    csv_data = ''
    # iterate through speeches
    for d in data:
        # all attributes must be found to store the data
        try:
            id_ = d['id']
            date = d['attributes']['dateStart'][:10]
            if d['attributes']['textContents'] != []:
                texts = d['attributes']['textContents'][0]['textBody']
                text = extract_speech(texts)
            else:
                text = None
            org_data = d['relationships']['organisations']['data']
            party = None
            for org_d in org_data:
                if org_d['attributes']['type'] == 'faction':
                    party = org_d['attributes']['labelAlternative']
            csv_data += f'{id_};;;{date};;;{party};;;{text}\n'
        except:
            print('Exception - occured while reading data from API')
    # save to .csv
    with open(os.path.join(os.path.dirname(__file__), 'data.csv'), 'a', encoding='utf-8') as f:
        f.write(csv_data)
    return date[:4]


def extract_speech(texts):
    """Link sentences in single string.
    """
    speech_text = ''
    for text in texts:
        if text['type'] == 'speech':
            for sentence in text['sentences']:
                speech_text = speech_text + sentence['text'] + ' '
    return speech_text
