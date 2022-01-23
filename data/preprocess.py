"""Utility functions for preprocessing the downloaded data.
"""

import re
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer


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
    r'Liebe Kolleginnen und Kollegen! ',
    r'Meine Damen und Herren! ',
    r'Herzlichen Dank.*\. ',
    r'Recht vielen Dank.*\. ',
    r'Ich danke (Ihnen)|(euch).*!|\.',
    r'.|!|\? .*N|nächste(r|n)* Red(nerin|er).*\.',
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
