import json
import os
import pandas as pd
import random
from sklearn.decomposition import LatentDirichletAllocation
from featurize import featurize


def fit_model(train_data, n_topics, n_docs=None, max_iter=5, random_state=0):
    if n_docs:
        train_data = random.sample(train_data, n_docs)
    lda_model = LatentDirichletAllocation(
        n_components=n_topics, max_iter=max_iter, random_state=random_state)
    lda_model.fit(train_data)
    return lda_model


def transform_docs(lda_model, train_data):
    return lda_model.transform(train_data)


def get_top_topic_words(lda_model, feature_names, n_words=10):
    topics = []
    for topic in lda_model.components_:
        top_features_ind = topic.argsort()[: -n_words - 1 : -1]
        top_features = [feature_names[i] for i in top_features_ind]
        weights = topic[top_features_ind]
        topics.append({n: w for n, w in zip(top_features, weights)})
    return topics


if __name__ == '__main__':
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'preprocessed_data.csv'))
    count_feats, feature_names = featurize(df, tfidf=True, max_df=0.5, min_df=5)
    lda_model = fit_model(count_feats, n_topics=6)
    transformed_data = transform_docs(lda_model, count_feats)
    topics = get_top_topic_words(lda_model, feature_names)
    for topic in range(len(topics)):
        df[f'Topic{topic}'] = transformed_data[:, topic]
    df.drop(columns='preprocessed_text', inplace=True)
    df.to_csv(os.path.join(os.path.dirname(__file__), 'transformed_data.csv'))
    with open(os.path.join(os.path.dirname(__file__), 'topics.json'), 'w') as f:
        json.dump(topics, f)
    for topic in topics:
        print(topic.keys())
