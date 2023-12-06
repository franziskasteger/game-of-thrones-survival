from got_survival.ml_logic.model_death_prediction import death_x_and_y, death_create_pipeline, \
    death_split_train, death_f1_score, death_create_pipeline_rf,death_f1_macro_score
from got_survival.ml_logic.model_episode_of_death import episode_x_and_y, \
    episode_create_pipeline, episode_split_train, episode_get_weights
import pickle
import pandas as pd
from sklearn.metrics import f1_score

# Random Forest
def death_train_RF() -> None:
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

def death_evaluate_RF() -> float:
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

def death_pred_RF(new_character:pd.DataFrame) -> int:
    '''
    Use the fitted logistic regression pipeline to predict whether a new
    character survives or not.
    '''
    # Load model
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model.pkl", "rb"))
    return death_pipe.predict(new_character)[0] # Return prediction


# Time of death
def episode_train() -> None:
    '''
    Will train a XGBClassifier pipeline to predict when a character dies.
    '''
    X, y = episode_x_and_y() # Import data and split it into features and target
    # Train-test-split with random state so that it is the same split for evaluating
    # X_train, X_test, y_train, y_test = episode_split_train(X, y)
    episode_pipe = episode_create_pipeline() # Create pipeline with preprocessor and model
    weights = episode_get_weights(y)
    episode_pipe.fit(X, y, xgbclassifier__sample_weight=weights) #.values.ravel()  # Fit pipeline

    with open("got_survival/models_pickle/episode_model.pkl", "wb") as file:
        pickle.dump(episode_pipe, file) # Save trained model for evaluation and prediction

def episode_evaluate() -> float:
    '''
    Evaluate the trained XGBClassifier pipeline.
    '''
    # Load trained model
    episode_pipe = pickle.load(open("got_survival/models_pickle/episode_model.pkl", "rb"))
    X, y = episode_x_and_y() # Import data
    # Train-test-split with random state so that it is the same split as training
    X_train, X_test, y_train, y_test = episode_split_train(X, y)
    # score = episode_pipe.score(X_test, y_test) # calculate score
    y_pred = episode_pipe.predict(X_test)
    score = f1_score(y_test, y_pred, average="macro")
    # maybe save the score somewhere?
    return score

def episode_pred(new_character:pd.DataFrame) -> int:
    '''
    Use the fitted logistic regression pipeline to predict when a new character
    dies.
    '''
    # Load model
    episode_pipe = pickle.load(open("got_survival/models_pickle/episode_model.pkl", "rb"))
    class_ = episode_pipe.predict(new_character)[0] # Return prediction
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

    # death_train_RF()
    # print(death_evaluate_RF())
    # print(death_pred_RF(new_X))

    # episode_train()
    # print(episode_evaluate())
    # print(episode_pred(new_X))
    pass
