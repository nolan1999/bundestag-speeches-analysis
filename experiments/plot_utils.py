import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from tueplots import bundles


def smoothed_df(df, window=21, std=3):
    margin = int((window - 1) / 2)
    return df.rolling(window=window, win_type='gaussian', center=True).mean(std=std)[margin:-margin]


def stacked_plot(df, subset=None):
    plt.rcParams.update(bundles.neurips2021(usetex=False))
    y=[]
    topics=[]
    cols = subset or df.columns
    for idx, topic_col in enumerate(cols):
        y.append(None)
        topics.append(topic_col)
        y[idx] = df[topic_col].values
    y = np.vstack([y])
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.stackplot(df.index.values, y, labels=topics, linewidth=2)
    ax.set_xlim(left=df.index.values.min(), right=df.index.values.max())
    if subset is None:
        ax.set_ylim(bottom=0., top=1.)
    else:
        ax.set_ylim(bottom=0.)
    ax.set_xlabel('Date')
    ax.set_ylabel('Topic weight')
    # revert legend order to follow stacked order
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='upper left')
    return fig


def topic_plot(df, topic):
    plt.rcParams.update(bundles.neurips2021(usetex=False))
    fig, ax = plt.subplots(figsize=(10, 4))
    # plot topic
    ax.plot(df.index.values, df[topic].values, label=f'{topic} weight')
    # plot mean
    mean = df[topic].values.mean()
    ax.hlines(mean, xmin=df.index.values.min() , xmax = df.index.values.max(), color='k', label='mean')
    # color regions
    std = df[topic].values.std()
    ax.fill_between(df.index.values, mean+2*std, df[topic].values, where=df[topic].values>mean+2*std,
                    interpolate=True, alpha=0.5, color='green', label='$\in (\mu+2\sigma, \infty)$')
    ax.fill_between(df.index.values, mean+std, df[topic].values, where=df[topic].values>mean+std,
                    interpolate=True, alpha=0.3, color='green', label='$\in (\mu+\sigma, \mu+2\sigma]$')
    ax.fill_between(df.index.values, mean, df[topic].values, where=df[topic].values>=mean,
                    interpolate=True, alpha=0.2, color='green', label='$\in (\mu, \mu+\sigma]$')
    ax.fill_between(df.index.values, df[topic].values, mean, where=df[topic].values<mean,
                    interpolate=True, alpha=0.2, color='red', label='$\in [\mu-\sigma, \mu)$')
    ax.fill_between(df.index.values, df[topic].values, mean-std, where=df[topic].values<mean-std,
                    interpolate=True, alpha=0.3, color='red', label='$\in [\mu-2\sigma, \mu+\sigma)$')
    ax.fill_between(df.index.values, df[topic].values, mean-2*std, where=df[topic].values<mean-2*std,
                    interpolate=True, alpha=0.5, color='red', label='$\in (-\infty, \mu-2\sigma)$')

    ax.set_xlim(left=df.index.values.min(), right=df.index.values.max())
    ax.set_xlabel('Date')
    ax.set_ylabel('Topic weight')
    ax.legend(loc='upper left')
    return fig


def pca_plot(df):
    plt.rcParams.update(bundles.neurips2021(usetex=False))
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    means = df.groupby('party').mean()
    pca = PCA(n_components=2)
    X_r = pca.fit_transform(means.to_numpy())
    fig, ax = plt.subplots(figsize=(7, 4))
    for party, x_r, color in zip(means.index, X_r, colors):
        ax.scatter(x_r[1], x_r[0], c=color)
        # move spd label away from fdp label
        if party == 'SPD':
            ax.annotate(party, (x_r[1]+0.008, x_r[0]-0.002), c=color)
        else:
            ax.annotate(party, (x_r[1]-0.001, x_r[0]-0.002), c=color)
    ax.set_xlim(left=-0.06)
    ax.invert_xaxis()
    ax.legend(loc='upper left')
    ax.set_xlabel('Second principal component')
    ax.set_ylabel('First principal component')
    return fig, pca


def sentiments_plot(df):
    plt.rcParams.update(bundles.neurips2021(usetex=False))

    parties = df['party'].unique()
    topics = df['topic'].unique()

    sent = np.array([
        [df[(df['party'] == party) * (df['topic'] == topic)]['sentiment_num'].mean()
            for topic in topics]
        for party in parties])
    total = np.array([
        [df[(df['party'] == party) * (df['topic'] == topic)]['sentiment_num'].count()
            for topic in topics]
        for party in parties])

    fig, ax = plt.subplots(figsize=(7, 4))
    im = ax.imshow(-sent, cmap='seismic')

    ax.set_xticks(np.arange(len(topics)), labels=topics)
    ax.set_yticks(np.arange(len(parties)), labels=parties)

    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")

    min_val = np.min(sent)
    max_val = np.max(sent)
    delta = max_val - min_val

    for i in range(len(parties)):
        for j in range(len(topics)):
            color = "w" if sent[i, j] < min_val + 0.3 * delta or sent[i, j] > min_val + 0.7 * delta else "k"
            ax.text(j, i, f'{round(sent[i, j], 2)} ({total[i, j]})', ha="center", va="center", color=color)

    return fig
