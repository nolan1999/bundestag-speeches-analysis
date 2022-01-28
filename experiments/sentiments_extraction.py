import importlib
import os
from models.extract_sentiments import extract_sentiments


def get_sentiments(params_path, subset=None):
    params = importlib.import_module(params_path)
    save_path = params.paths['save_path']
    df = extract_sentiments(params.paths['unprocessed_data_path'], subset)
    # Store data
    df.to_csv(os.path.join(save_path, 'sentiments_data.csv'))
