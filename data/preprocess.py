import re


PARTIES = [
    'SPD',
    'FDP',
    'CDU/CSU',
    'BÜNDNIS 90/DIE GRÜNEN',
    'AfD',
    'DIE LINKE',
]


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


def filter_parties(df, parties):
    return df[df.party.isin(parties)]


def remove_formalities(string):
    for expr in EXPRS:
        string = re.sub(expr, '', string)
    return string


def remove_stopwords(string):
    pass


def stem(string):
    pass


def featurize(string):
    pass
