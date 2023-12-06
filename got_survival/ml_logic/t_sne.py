import pandas as pd
from sklearn.manifold import TSNE
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


def get_tsne(new_X:pd.DataFrame) -> plt.Axes:
    houses = pd.read_csv('features_for_quiz/houses/classes.csv')
    X = houses.drop(columns='class')
    y = houses['class']
    X_with_new = pd.concat((X, new_X)).reset_index(drop=True)
    y_with_new = pd.concat((y, pd.Series('You'))).reset_index(drop=True)

    tsne_new = TSNE(n_components=2, perplexity=3, init='random', n_iter=1_000_000, random_state=4)
    X_with_new_emb = pd.DataFrame(tsne_new.fit_transform(X_with_new), columns=tsne_new.get_feature_names_out())
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    markers = ['o', 'x', '*', '2']

    f, ax = plt.subplots()
    c = 0
    s = 0
    n = 0
    for i in range(len(X_with_new_emb)-1):
        ax.scatter(X_with_new_emb.loc[i][0], X_with_new_emb.loc[i][1], c=colors[c%5],
                    marker=markers[s%4], label=y_with_new[i])
        c += 1
        s += 1
        n += 1
    ax.scatter(X_with_new_emb.iloc[-1][0], X_with_new_emb.iloc[-1][1], c='black',
                marker='X', label=y_with_new.iloc[-1])
    ax.legend(bbox_to_anchor=(1, 1.1))

    ax.set_xticks([])
    ax.set_yticks([])

    return ax


new_character = {
    'outcast': [0],
    'climate': [2],
    'empathy': [4],
    'fighting': [3],
    'honor': [4],
    'connections': [2],
    'unyielding': [5]
}
X = pd.DataFrame.from_dict(new_character)


if __name__ == '__main__':

    # ax = get_tsne(X)
    # plt.show()

    pass
