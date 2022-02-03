import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from tueplots import bundles


def adapt_figsize(ratio=2.):
    default_width = plt.rcParams['figure.figsize'][0]
    return (default_width, round(default_width/ratio, 2))


def smoothed_df(df, window=21, std=3):
    return df.rolling(window=window, win_type='gaussian', center=True, min_periods=1).mean(std=std)


def stacked_plot(df, subset=None):
    y=[]
    topics=[]
    #color_map = ["#003f5c", "#2f4b7c", "#665191", "#a05195", "#d45087", "#f95d6a", "#ff7c43", "#ffa600", "#FFCC00"]
    color_map = ["#003f5c", "#f95d6a", "#2f4b7c", "#ff7c43", "#665191", "#ffa600", "#a05195", "#FFCC00", "#d45087"]
    cols = subset or df.columns
    for idx, topic_col in enumerate(cols):
        y.append(None)
        topics.append(topic_col)
        y[idx] = df[topic_col].values
    y = np.vstack([y])
    with plt.rc_context(bundles.neurips2021(usetex=False,family='serif')):
        ratio = 2.
        fig, ax = plt.subplots(figsize=adapt_figsize(ratio))
        ax.stackplot(df.index.values, y, labels=topics, linewidth=2, colors = color_map)
        ax.set_xlim(left=df.index.values.min(), right=df.index.values.max())
        if subset is None:
            ax.set_ylim(bottom=0., top=1.)
        else:
            ax.set_ylim(bottom=0.)
        ax.set_xlabel('Date')
        ax.set_ylabel('Topic weight')
        # revert legend order to follow stacked order
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], framealpha=0.5, loc='upper left', prop={'weight':'bold'})
    return fig


def topic_plot(df, topic):
    with plt.rc_context(bundles.neurips2021(usetex=False,family='serif')):
        ratio = 2.5
        fig, ax = plt.subplots(figsize=adapt_figsize(ratio))
        # plot topic
        ax.plot(df.index.values, df[topic].values, label=f'{topic} weight')
        # plot mean
        mean = df[topic].values.mean()
        #ax.hlines(mean, xmin=df.index.values.min() , xmax = df.index.values.max(), color='yellow', label='Mean')
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
        ax.legend(framealpha=0.5, loc='upper right',ncol=2)
    return fig


def pca_plot(df):
    with plt.rc_context(bundles.neurips2021(usetex=False,family='serif')):
        colors = {
            'DIE LINKE': 'purple',
            'AfD': 'blue',
            'BÜNDNIS 90/DIE GRÜNEN': 'green',
            'SPD': 'red',
            'FDP': 'yellow',
            'CDU/CSU': 'black',
        }
        means = df.groupby('party').mean()
        pca = PCA(n_components=2)
        X_r = pca.fit_transform(means.to_numpy())
        ratio = 2.
        fig, ax = plt.subplots(figsize=adapt_figsize(ratio))
        for party, x_r in zip(means.index, X_r):
            color = colors[party]
            ax.scatter(x_r[1], x_r[0], c=color)
            # move spd label away from fdp label
            if party == 'SPD':
                ax.annotate(party, (x_r[1]+0.009, x_r[0]-0.003), c=color)
            else:
                ax.annotate(party, (x_r[1]-0.002, x_r[0]-0.003), c=color)
        ax.set_xlim(left=-0.06)
        ax.invert_xaxis()
        ax.set_xlabel('Second principal component')
        ax.set_ylabel('First principal component')
    return fig, pca


def sentiments_plot(df):
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

    with plt.rc_context(bundles.neurips2021(usetex=False, family='serif')):
        ratio = 2.5
        fig, ax = plt.subplots(figsize=adapt_figsize(ratio))
        im = ax.imshow(-sent, cmap='seismic')

        parties_labels = [p.replace('BÜNDNIS 90/', '') for p in parties]
        parties_labels = parties
        ax.set_xticks(np.arange(len(topics)), labels=topics)
        ax.set_yticks(np.arange(len(parties)), labels=parties_labels)

        plt.setp(ax.get_xticklabels(), rotation=30, ha="right", rotation_mode="anchor")

        min_val = np.min(sent)
        max_val = np.max(sent)
        delta = max_val - min_val

        for i in range(len(parties)):
            for j in range(len(topics)):
                color = "w" if sent[i, j] < min_val + 0.3 * delta or sent[i, j] > min_val + 0.7 * delta else "k"
                ax.text(j, i, f'{round(sent[i, j], 2)} \n ({total[i, j]})', ha="center", va="center", color=color, fontsize=4)

    return fig
