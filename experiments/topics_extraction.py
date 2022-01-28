import importlib
import json
import os
import matplotlib.pyplot as plt
from tueplots import bundles
from math import ceil
from models.extract_topics import extract_topics


def get_topics(params_path):
    params = importlib.import_module(params_path)
    save_path = params.paths['save_path']
    df, topics = extract_topics(params.paths['input_data_path'], **params.topic_extraction_params)
    fig = plot_topics(topics, **params.topic_plot_params)
    # Store data
    df.to_csv(os.path.join(save_path, 'transformed_data.csv'))
    with open(os.path.join(save_path, 'topics.json'), 'w') as f:
        json.dump(topics, f)
    fig.savefig(os.path.join(save_path, 'topics_words.pdf'))
    return df, topics


def plot_topics(topics, title='Top predictor features', n_words=9):
    plt.rcParams.update(bundles.neurips2021(usetex=False))
    # Source: https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
    n_cols = 3
    n_rows = ceil(len(topics)/n_cols)
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, int(n_rows*5*n_words/10)))
    axes = axes.flatten()
    for topic_idx, topic in enumerate(topics):
        top_features = list(topic.items())[:n_words]
        words = [f[0] for f in top_features]
        weights = [f[1] for f in top_features]
        ax = axes[topic_idx]
        ax.barh(words, weights)
        ax.set_title(f"Topic{topic_idx}", fontsize=20)
        ax.invert_yaxis()
        ax.tick_params(axis="both", which="major", labelsize=20)
    fig.suptitle(title, fontsize=30)
    return fig
