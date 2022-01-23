from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def featurize(df, tfidf=False, col='preprocessed_text', min_df=1, max_df=1.0):
    featurizer = (TfidfVectorizer if tfidf else CountVectorizer)(
        min_df=min_df, max_df=max_df)
    count_feats = featurizer.fit_transform(df[col])
    feature_names = featurizer.get_feature_names_out()
    return count_feats, feature_names
