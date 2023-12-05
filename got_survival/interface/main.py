from got_survival.ml_logic.model_death_prediction import death_x_and_y, death_create_pipeline, \
    death_split_train, death_f1_score, death_create_pipeline_rf,death_f1_macro_score
from got_survival.ml_logic.model_episode_of_death import episode_x_and_y, \
    episode_create_pipeline, episode_split_train
import pickle
import pandas as pd
from sklearn.metrics import f1_score

#For Random Forest
def death_train_RF() -> None:
    '''
    Will train a logistic regression pipeline to predict whether a character
    survives or not.
    '''
    X, y = death_x_and_y() # Import data and split it into features and target
    # Train-test-split with random state so that it is the same split for evaluating
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    pipe = death_create_pipeline_rf() # Create pipeline with preprocessor and model
    pipe.fit(X_train, y_train.values.ravel()) # Fit pipeline

    with open("got_survival/models_pickle/death_model_RF.pkl", "wb") as file:
        pickle.dump(pipe, file) # Save trained model for evaluation and prediction

def death_evaluate_RF() -> float:
    '''
    Evaluate the trained logistic regression pipeline.
    '''
    # Load trained model
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model_RF.pkl", "rb"))
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
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model_RF.pkl", "rb"))
    return death_pipe.predict(new_character)[0] # Return prediction


#For logistic regression
def death_train() -> None:
    '''
    Will train a logistic regression pipeline to predict whether a character
    survives or not.
    '''
    X, y = death_x_and_y() # Import data and split it into features and target
    # Train-test-split with random state so that it is the same split for evaluating
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    pipe = death_create_pipeline() # Create pipeline with preprocessor and model
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


def episode_train() -> None:
    '''
    Will train a XGBClassifier  pipeline to predict when a character dies.
    '''
    X, y = episode_x_and_y() # Import data and split it into features and target
    # Train-test-split with random state so that it is the same split for evaluating
    X_train, X_test, y_train, y_test = episode_split_train(X, y)
    episode_pipe = episode_create_pipeline() # Create pipeline with preprocessor and model
    episode_pipe.fit(X_train, y_train) #.values.ravel()  # Fit pipeline

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
    return round(episode_pipe.predict(new_character)[0][0]) # Return prediction


###########################
########## TESTS ##########
###########################

test = {
    'male': [0],
    'origin': ["House Stark"],
    'isMarried': [0],
    'isNoble': [1],
    'popularity': [0.753]
}
new_X = pd.DataFrame.from_dict(test)

if __name__ == '__main__':
    print(f'-----------------Logistic Regression-------------------------')
    death_train()
    print(death_evaluate())
    print(death_pred(new_X))

    print(f'------------------------------------------')
    print(f'-----------------Random Forest-------------------------')
    death_train_RF()
    print(death_evaluate_RF())
    print(death_pred_RF(new_X))

    # episode_train()
    # print(episode_evaluate())
    # print(episode_pred(new_X))
    #pass
