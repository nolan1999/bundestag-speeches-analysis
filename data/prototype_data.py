"""Download data using openparliament.tv API for prototyping.
"""

import os
from api import get_data


if __name__ == '__main__':
    options = {
        'dateFrom': '2018-01-01',
        'dateTo': '2018-12-31',
    }
    df = get_data(options)
    df.to_csv(os.path.join(os.path.dirname(__file__),
            'prototype_data.csv'))
