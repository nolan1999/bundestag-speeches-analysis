import os


dir_path = os.path.dirname(__file__)

topic_extraction_params = {
    'model': 'LatentDirichletAllocation',
    'n_topics': 9,
    'tfidf': False,
    'max_df': 0.3,
    'min_df': 20,
    'max_iter': 250,
    'stem': True,
    'random_state':42
}

topic_plot_params = {
    'n_words': 10,
}

paths = {
    'input_data_path': os.path.join(dir_path, '..', '..', 'data', 'preprocessed_data.csv'),
    'save_path': dir_path,
}
