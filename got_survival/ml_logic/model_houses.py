import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import pickle

def houses_model_train():
    '''
    Trains the model for the prediction of origin of a new character
    '''
    # Read data
    house = pd.read_csv('features_for_quiz/houses/classes.csv')

    # Split the data based on 'outcast'
    outcasts = house[house['outcast'] == 1]
    not_outcasts = house[house['outcast'] == 0]

    # Create X and y
    outcasts_X = outcasts.drop(columns='class')
    outcasts_y = outcasts['class']
    not_outcasts_X = not_outcasts.drop(columns='class')
    not_outcasts_y = not_outcasts['class']
    X = house.drop(columns='class')
    y = house['class']

    # Initiate models
    model_outcasts = KNeighborsClassifier(n_neighbors=1)
    model_not_outcasts = KNeighborsClassifier(n_neighbors=1)
    model = KNeighborsClassifier(n_neighbors=1)

    # Train models
    model_outcasts.fit(outcasts_X, outcasts_y)
    model_not_outcasts.fit(not_outcasts_X, not_outcasts_y)
    model.fit(X, y)

    # Save models
    with open('got_survival/models_pickle/outcasts.pkl', 'wb') as file:
        pickle.dump(model_outcasts, file)

    with open('got_survival/models_pickle/not_outcasts.pkl', 'wb') as file:
        pickle.dump(model_not_outcasts, file)

    with open('got_survival/models_pickle/houses.pkl', 'wb') as file:
        pickle.dump(model, file)

def houses_model_predict(X:pd.DataFrame, based_on_outcast:bool=True) -> str:
    '''
    Predicts the house for a given character
    '''
    # Checks for 'outcast' and uses correct model, returns prediction
    if X['outcast'][0]:
        model_outcasts = pickle.load(open('got_survival/models_pickle/outcasts.pkl', 'rb'))
        return model_outcasts.predict(X)[0]

    model_not_outcasts = pickle.load(open('got_survival/models_pickle/not_outcasts.pkl', 'rb'))
    return model_not_outcasts.predict(X)[0]





###########################
########## TESTS ##########
###########################

new_character = {
    'outcast': [1],
    'climate': [2],
    'empathy': [3],
    'fighting': [3],
    'honor': [3],
    'connections': [3],
    'unyielding': [3]
}
X = pd.DataFrame.from_dict(new_character)

if __name__ == '__main__':

    # houses_model_train()
    print(houses_model_predict(X))
    pass
