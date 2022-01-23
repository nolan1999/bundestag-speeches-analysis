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


def get_topics(lda_model):
    return lda_model.components_
