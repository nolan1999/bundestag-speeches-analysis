import os


dir_path = os.path.dirname(__file__)

topic_extraction_params = {
    'model': 'NMF',
    'n_topics': 6,
    'tfidf': True,
    'max_df': 0.5,
    'min_df': 5,
}

topic_plot_params = {
    'n_words': 10,
}

paths = {
    'input_data_path': os.path.join(dir_path, '..', '..', 'data', 'preprocessed_data.csv'),
    'save_path': dir_path,
}
