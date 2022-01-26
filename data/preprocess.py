"""Utility functions for preprocessing the downloaded data.
"""

import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer


def preprocess_data(data_path, preprocessed_data_path):
    """Function for preprocessing pipeline.
    """
    df = pd.read_csv(data_path, sep=';;;', header=0)
    # remove duplicates
    df.drop_duplicates(subset='id', inplace=True)
    df = df[df.text != 'None']
    df.set_index('id', inplace=True)
    df = filter_parties(df, PARTIES)
    preprocess(df)
    df.to_csv(preprocessed_data_path)


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


def get_preprocessor(stem=True, remove_stopwords=True):
    """Preprocesses text: separate words, remove stopwords, stem.
    """
    #TODO: parallelize
    de_stopwords = stopwords.words('german') if remove_stopwords else []
    stemmer = SnowballStemmer('german', ignore_stopwords=True).stem if stem else lambda x: x
    analyzer = CountVectorizer().build_analyzer()
    return lambda text: ' '.join(
        [(stemmer(w)) for w in analyzer(text)
        if w not in de_stopwords])


def preprocess(df, col='text'):
    """Processing of each text.
    """
    prepr = get_preprocessor()
    prepr_no_stemming = get_preprocessor(stem=False)
    df['preprocessed_text'] = df[col].apply(lambda t: prepr(remove_formalities(t)))
    df['preprocessed_unstemmed_text'] = df[col].apply(lambda t: prepr_no_stemming(remove_formalities(t)))
    df.drop(columns='text', inplace=True)
