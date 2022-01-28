from experiments.topics_extraction import get_topics
from experiments.sentiments_extraction import get_sentiments


df, _ = get_topics('experiments.exp03.params')
subset = df.index
get_sentiments('experiments.exp03.params', subset=subset)
