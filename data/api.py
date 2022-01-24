#-*-coding: utf-8-*-
"""API connection and storing functions.
"""

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
        # start from where it left off
        with open(file_path, 'r', encoding='utf-8') as f:
            year, page = f.read().split(';')
            year = int(year)
            page = int(page) + 1
    except:
        # if first call, start from initial data
        year = 2017
        page = 1
        with open(os.path.join(os.path.dirname(__file__), 'data.csv'), 'w', encoding='utf-8') as f:
            f.write('id, date, party, text\n')
    # next page
    # get one page at a time (10 speeches)
    for _ in range(n_pages):
        get_data({'dateFrom': f'{year}-01-01', 'page': page})
        # store states
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f'{year};{page}')
        page += 1
        if page > MAX_PAGES:
            year += 1
            if year > CURRENT_YEAR:
                return
            page = 1


def get_data(options):
    json_data = send_request(options)
    if json_data['meta']['results']['count']:
        extract_data_from_json(json_data)


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
            texts = d['attributes']['textContents'][0]['textBody']
            text = extract_speech(texts)
            org_data = d['relationships']['organisations']['data']
            party = None
            for org_d in org_data:
                if org_d['attributes']['type'] == 'faction':
                    party = org_d['attributes']['labelAlternative']
            csv_data += f'{id_};;;{date};;;{party};;;{text}\n'
        except:
            print('fail')
    # save to .csv
    with open(os.path.join(os.path.dirname(__file__), 'data.csv'), 'a', encoding='utf-8') as f:
        f.write(csv_data)


def extract_speech(texts):
    """Link sentences in single string.
    """
    speech_text = ''
    for text in texts:
        if text['type'] == 'speech':
            for sentence in text['sentences']:
                speech_text = speech_text + sentence['text'] + ' '
    return speech_text
