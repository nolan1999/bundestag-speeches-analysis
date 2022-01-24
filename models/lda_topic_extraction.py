import random
from sklearn.decomposition import LatentDirichletAllocation


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
        topics.append((weights, top_features))
    return topics
