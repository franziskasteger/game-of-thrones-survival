from got_survival.ml_logic.model_death_prediction import death_x_and_y, death_create_pipeline, \
    death_split_train, death_f1_macro_score
from got_survival.ml_logic.model_season_of_death import season_x_and_y, \
    season_create_pipeline, season_split_train, season_get_weights
import pickle
import pandas as pd
from sklearn.metrics import f1_score

# Random Forest
def death_train() -> None:
    '''
    Will train a logistic regression pipeline to predict whether a character
    survives or not.
    '''
    X, y = death_x_and_y() # Import data and split it into features and target
    # Train-test-split with random state so that it is the same split for evaluating
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    pipe = death_create_pipeline(y_train) # Create pipeline with preprocessor and model
    pipe.fit(X_train, y_train.values.ravel()) # Fit pipeline

    with open("got_survival/models_pickle/death_model.pkl", "wb") as file:
        pickle.dump(pipe, file) # Save trained model for evaluation and prediction

def death_evaluate() -> float:
    '''
    Evaluate the trained logistic regression pipeline.
    '''
    # Load trained model
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model.pkl", "rb"))
    X, y = death_x_and_y() # Import data
    # Train-test-split with random state so that it is the same split as training
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    y_pred = death_pipe.predict(X_test) # predict X_test with pipeline
    score = death_f1_macro_score(y_test, y_pred) # calculate score
    # maybe save the score somewhere?
    return score

def death_pred(new_character:pd.DataFrame) -> int:
    '''
    Use the fitted logistic regression pipeline to predict whether a new
    character survives or not.
    '''
    # Load model
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model.pkl", "rb"))
    return death_pipe.predict(new_character)[0] # Return prediction


# Time of death
def season_train() -> None:
    '''
    Will train a XGBClassifier pipeline to predict when a character dies.
    '''
    X, y = season_x_and_y() # Import data and split it into features and target
    # Train-test-split with random state so that it is the same split for evaluating
    # X_train, X_test, y_train, y_test = season_split_train(X, y)
    episode_pipe = season_create_pipeline() # Create pipeline with preprocessor and model
    weights = season_get_weights(y)
    episode_pipe.fit(X, y, xgbclassifier__sample_weight=weights) #.values.ravel()  # Fit pipeline

    with open("got_survival/models_pickle/season_model.pkl", "wb") as file:
        pickle.dump(episode_pipe, file) # Save trained model for evaluation and prediction

def season_evaluate() -> float:
    '''
    Evaluate the trained XGBClassifier pipeline.
    '''
    # Load trained model
    season_pipe = pickle.load(open("got_survival/models_pickle/season_model.pkl", "rb"))
    X, y = season_x_and_y() # Import data
    # Train-test-split with random state so that it is the same split as training
    X_train, X_test, y_train, y_test = season_split_train(X, y)
    # score = season_pipe.score(X_test, y_test) # calculate score
    y_pred = season_pipe.predict(X_test)
    score = f1_score(y_test, y_pred, average="macro")
    # maybe save the score somewhere?
    return score

def season_pred(new_character:pd.DataFrame) -> int:
    '''
    Use the fitted logistic regression pipeline to predict when a new character
    dies.
    '''
    # Load model
    season_pipe = pickle.load(open("got_survival/models_pickle/season_model.pkl", "rb"))
    class_ = season_pipe.predict(new_character)[0] # Return prediction
    return class_ + 1

###########################
########## TESTS ##########
###########################

test = {
    'male': [1],
    'origin': ["Peasant"],
    'isMarried': [1],
    'isNoble': [0],
    'popularity': [0.1]
}
new_X = pd.DataFrame.from_dict(test)

if __name__ == '__main__':

    # death_train()
    # print(death_evaluate())
    # print(death_pred(new_X))

    # season_train()
    # print(season_evaluate())
    print(season_pred(new_X))
    pass
