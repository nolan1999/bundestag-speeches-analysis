import pandas as pd
from germansentiment import SentimentModel


def extract_sentiments(input_data_path, subset=None):
    """Extract sentiments from speeches.
    """
    df = pd.read_csv(input_data_path, index_col='id', sep=';;;')
    if subset is not None:
        df = df.loc[subset]
    model = SentimentModel()
    sentiments = []
    batch_size = 128
    for start_index in range(0, df.shape[0], batch_size):
        sentiments = sentiments + model.predict_sentiment(df['text'][start_index:min(start_index+batch_size, df.shape[0])])
        print(start_index+batch_size)
    df['sentiment'] = sentiments
    df.drop(columns='text', inplace=True)
    return df
