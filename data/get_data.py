"""Download data using openparliament.tv API.
"""

import os
from api import get_pages
from preprocess import preprocess_data


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    data_path = os.path.join(dirname, 'data.csv')
    state_path = os.path.join(dirname, 'state.txt')
    preprocessed_data_path = os.path.join(dirname, 'preprocessed_data.csv')

    get_pages(
        n_pages=10000,
        data_path=data_path,
        state_path=state_path,
    )

    preprocess_data(
        data_path=data_path,
        preprocessed_data_path=preprocessed_data_path,
    )
