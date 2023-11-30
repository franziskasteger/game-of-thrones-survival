from got_survival.ml_logic.model_death_prediction import death_x_and_y, death_create_pipeline, \
    death_split_train, death_f1_score
from got_survival.ml_logic.model_episode_of_death import episode_x_and_y, \
    episode_create_pipeline, episode_split_train, episode_prediction
import pickle
import pandas as pd
from math import ceil

def death_train():
    X, y = death_x_and_y()
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    pipe = death_create_pipeline()
    pipe.fit(X_train, y_train.values.ravel())

    # we should save the model somewhere instead of returning it
    with open("got_survival/models_pickle/death_model.pkl", "wb") as file:
        pickle.dump(pipe, file)

def death_evaluate():
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model.pkl", "rb"))
    X, y = death_x_and_y()
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    y_pred = death_pipe.predict(X_test)
    score = death_f1_score(y_test, y_pred)
    # maybe save the score somewhere?
    return score

def death_pred(new_character):
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model.pkl", "rb"))
    return int(death_pipe.predict(new_character)[0])


def episode_train():
    X, y = episode_x_and_y()
    X_train, X_test, y_train, y_test = episode_split_train(X, y)
    episode_pipe = episode_create_pipeline()
    episode_pipe.fit(X_train, y_train) #.values.ravel()

    # we should save the model somewhere instead of returning it
    with open("got_survival/models_pickle/episode_model.pkl", "wb") as file:
        pickle.dump(episode_pipe, file)

def episode_evaluate():
    # if we save the model somewhere, we should load it instead of passing it to the function
    episode_pipe = pickle.load(open("got_survival/models_pickle/episode_model.pkl", "rb"))
    X, y = episode_x_and_y()
    X_train, X_test, y_train, y_test = episode_split_train(X, y)
    score = episode_pipe.score(X_test, y_test)
    # maybe save the score somewhere?
    return score

def episode_pred(new_character):
    episode_pipe = pickle.load(open("got_survival/models_pickle/episode_model.pkl", "rb"))
    return ceil(episode_pipe.predict(new_character)[0])

test = {
    'male': [0],
    'origin': ["House Stark"],
    'isMarried': [0],
    'isNoble': [1],
    'popularity': [0.753]
}


########## TESTS ##########
if __name__ == '__main__':
    # death_train()
    # print(death_evaluate())
    # print(death_pred(new_X))

    # episode_train()
    # print(episode_evaluate())
    # print(episode_pred(test))
    pass
