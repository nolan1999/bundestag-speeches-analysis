from operator import index
import pandas as pd
import numpy as np
import random
from sklearn.decomposition import NMF, LatentDirichletAllocation
from models.featurize import featurize
from scipy.sparse import csr_matrix

def extract_topics(input_data_path, model='LatentDirichletAllocation',
                n_topics=6, tfidf=True, max_df=0.5, min_df=5, max_iter=200, stem=True, random_state=0):
    """Extract topics from speeches.
    Featurize, train model, transform documents.
    Returns model's words and transformed documents.
    """
    # Featurize
    df = pd.read_csv(input_data_path, index_col='id')
    col = 'preprocessed_text' if stem else 'preprocessed_unstemmed_text'
    count_feats, feature_names = featurize(df, tfidf=tfidf, max_df=max_df, min_df=min_df, col=col)
    # Train model and transform data
    trained_model = fit_model(count_feats, n_topics, model, max_iter, random_state=random_state)
    transformed_data = transform_docs(trained_model, count_feats)
    # Extract topic features
    topics = get_topic_words(trained_model, feature_names)
    for topic in range(len(topics)):
        df[f'Topic{topic}'] = transformed_data[:, topic]
    df.drop(columns=['preprocessed_text', 'preprocessed_unstemmed_text'], inplace=True)
    return df, topics


def fit_model(train_data, n_topics, model, max_iter, n_docs=None, random_state=0):
    """Fit the specified model to the passed data.
    """
    #train_data = create_sparse_matrix(train_data)
    if n_docs:
        train_data = random.sample(train_data, n_docs)
    trained_model = eval(model)(
        n_components=n_topics, random_state=random_state, max_iter=max_iter)  
    trained_model.fit(train_data)
    return trained_model


def create_sparse_matrix(df):
    df = csr_matrix(df.astype(np.float))
    return df


def transform_docs(trained_model, train_data):
    """Transform data.
    """
    return trained_model.transform(train_data)


def get_topic_words(trained_model, feature_names):
    """Get sorted predictors for each topic.
    """
    topics = []
    for topic in trained_model.components_:
        features_ind = topic.argsort()[::-1]
        features = [feature_names[i] for i in features_ind]
        weights = topic[features_ind]
        topics.append({n: w for n, w in zip(features, weights)})
    return topics
