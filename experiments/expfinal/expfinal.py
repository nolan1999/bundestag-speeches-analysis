from experiments.topics_extraction import get_topics
from experiments.sentiments_extraction import get_sentiments


df, _ = get_topics('experiments.expfinal.params')
subset = df.index
get_sentiments('experiments.expfinal.params', subset=subset)