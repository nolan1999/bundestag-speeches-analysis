"""Utility functions for preprocessing the downloaded data.
"""

import os
import pandas as pd
import re
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer


def preprocess_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data.csv'), sep=';;;', header=0)
    # remove duplicates
    df.drop_duplicates(subset='id', inplace=True)
    df.set_index('id', inplace=True)
    df = filter_parties(df, PARTIES)
    preprocess(df)
    df.to_csv(os.path.join(os.path.dirname(__file__), 'preprocessed_data.csv'))


# Parties of interest
PARTIES = [
    'SPD',
    'FDP',
    'CDU/CSU',
    'BÜNDNIS 90/DIE GRÜNEN',
    'AfD',
    'DIE LINKE',
]


# Repeated expressions empty of content
#TODO: complete list
EXPRS = [
    r'Herr Präsident! ',
    r'Frau Präsidentin! ',
    r'((l|L)ieben?|(m|M)einen?|(s|S)ehr geehrten?|(s|S)ehr verehrten?)+ (Kolleginnen und Kollegen|Damen und Herren)! ',
    r'(Herzlichen|Recht vielen) Dank\. ',
    r'Ich danke (Ihnen|euch)(!|\.) ',
    r'D|d(er|ie) N|nächste(r|n)? Red(nerin|er).*\.',
]


def filter_parties(df, parties, col='party'):
    """Keep speeches with defined parties only.
    """
    return df[df[col].isin(parties)]


def remove_formalities(string):
    """Remove formalities (expressions empty of content).
    """
    for expr in EXPRS:
        string = re.sub(expr, '', string)
    return string


def get_preprocessor():
    """Preprocesses text: separate words, remove stopwords, stem.
    """
    #TODO: parallelize
    stemmer = SnowballStemmer('german', ignore_stopwords=True)
    analyzer = CountVectorizer().build_analyzer()
    return lambda text: ' '.join([stemmer.stem(w) for w in analyzer(text)])


def preprocess(df, col='text'):
    prepr = get_preprocessor()
    preprocess_fn = lambda t: prepr(remove_formalities(t))
    df['preprocessed_text'] = df[col].apply(preprocess_fn)
    df.drop(columns='text', inplace=True)


if __name__ == '__main__':
    preprocess_data()
