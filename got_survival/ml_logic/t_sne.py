import pandas as pd
from sklearn.manifold import TSNE
import plotly.express as px
import matplotlib.pyplot as plt

def get_tsne(
        outcast:str,
        warm:str,
        empathy:int,
        fighting:int,
        honor:int,
        connections:int,
        unyielding:int
    ) -> plt.Axes:

    if warm == 'Warm':
        climate = 2
    elif warm == 'Medium':
        climate = 1
    else:
        climate = 0

    if outcast == 'No':
        outcast = 0
    else:
        outcast = 1

    new_X = pd.DataFrame.from_dict({
        'outcast': [outcast],
        'climate': [climate],
        'empathy': [empathy],
        'fighting': [fighting],
        'honor': [honor],
        'connections': [connections],
        'unyielding': [unyielding]
    })

    houses = pd.read_csv('features_for_quiz/houses/classes.csv')
    X = houses.drop(columns='class')
    y = houses['class']
    X_with_new = pd.concat((X, new_X)).reset_index(drop=True)
    y_with_new = pd.concat((y, pd.Series('You'))).reset_index(drop=True)

    tsne_new = TSNE(n_components=2, perplexity=3, init='random',
                    n_iter=1_000_000, random_state=4)
    X_with_new_emb = pd.DataFrame(tsne_new.fit_transform(X_with_new),
                                  columns=tsne_new.get_feature_names_out())


    fig = px.scatter(x=X_with_new_emb.iloc[:20, 0], y=X_with_new_emb.iloc[:20, 1],
                    text=y_with_new[:20], color=y_with_new[:20], size=pd.Series([10]*20))
    fig.update_traces(mode='markers', hovertemplate="%{text}")
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.add_scatter(x=X_with_new_emb.iloc[-1:, 0], y=X_with_new_emb.iloc[-1:, 1],
                    hovertemplate='You', name='You', showlegend=False,
                    marker=dict(size=25, color="Red", symbol='x'))
    fig.update_layout(dict1={'plot_bgcolor': 'rgba(0, 0, 0, 0.2)',
                             'paper_bgcolor': 'rgba(0, 0, 0, 0.2)'})
    #fig.update_layout(legend=dict(orientation="h", y=-0.2, x=0.5, xanchor='center'))
    fig.update_layout(showlegend=False)

    return fig

###########################
########## TESTS ##########
###########################

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

    # get_tsne(2, 'Warm', 3, 2, 4, 3, 3).show()

    pass
