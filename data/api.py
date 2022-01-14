import pandas as pd
import requests


URL_BASE = 'https://de.openparliament.tv/api/v1/search/media/'


def get_data(options):
    json_data = send_request(options)
    speeches_df = extract_df_from_json(json_data)
    return speeches_df


def send_request(options):
    url = f'{URL_BASE}?{"&".join([f"{k}={v}" for k, v in options.items()])}'
    return requests.get(url).json()


def extract_df_from_json(json_data):
    data = json_data['data']
    speeches = []
    ids = []
    for d in data:
        print(d)
        id_ = d['id']
        date = d['attributes']['dateStart'][:10]
        texts = d['attributes']['textContents'][0]['textBody']
        text = extract_speech(texts)
        org_data = d['relationships']['organisations']['data']
        party = None
        for org_d in org_data:
            if org_d['attributes']['type'] == 'faction':
                party = org_d['attributes']['labelAlternative']
        ids.append(id_)
        speeches.append((date, party, text))
    df = pd.DataFrame(speeches, columns=[
        'date', 'party', 'text'], index=ids)
    return df


def extract_speech(texts):
    speech_text = ''
    for text in texts:
        if text['type'] == 'speech':
            for sentence in text['sentences']:
                speech_text = speech_text + sentence['text'] + ' '
    return speech_text
