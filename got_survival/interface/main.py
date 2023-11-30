from got_survival.ml_logic.model_death_prediction import death_x_and_y, death_create_pipeline, death_split_train
from got_survival.ml_logic.model_episode_of_death import episode_read_data, episode_x_and_y, episode_create_pipeline, episode_split_train, episode_model, episode_cross_validate_result, episode_prediction
#from sklearn.linear_model import LogisticRegression
import pickle
import pandas as pd

def death_train():
    X, y = death_x_and_y()
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    pipe = death_create_pipeline()
    pipe.fit(X_train, y_train.values.ravel())

    # we should save the model somewhere instead of returning it
    with open("got_survival/models_pickle/death_model.pkl", "wb") as file:
        pickle.dump(pipe, file)

def death_evaluate():
    # if we save the model somewhere, we should load it instead of passing it to the function
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model.pkl", "rb"))
    X, y = death_x_and_y()
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    score = death_pipe.score(X_test, y_test)
    # maybe save the score somewhere?
    return score

def death_pred(new_character):
    death_pipe = pickle.load(open("got_survival/models_pickle/death_model.pkl", "rb"))
    return int(death_pipe.predict(new_character)[0])

#print(death_evaluate())


def episode_train():
    X, y = episode_x_and_y()
    X_train, X_test, y_train, y_test = episode_split_train(X, y)
    episode_pipe = episode_create_pipeline()
    episode_pipe.fit(X_train, y_train.values.ravel())

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

def episode_pred(episode_new_character):
    episode_pipe = pickle.load(open("got_survival/models_pickle/episode_model.pkl", "rb"))
    return int(episode_pipe.predict(episode_new_character)[0])

test = {
    'male': [0],
    'origin': ["House Stark"],
    'book1': [1],
    'book2': [1],
    'book3': [1],
    'book4': [1],
    'book5': [1],
    'isMarried': [0],
    'isNoble': [1],
    'numDeadRelations': [3],
    'boolDeadRelations': [1],
    'popularity': [0.753],
    'episode_global_num': [43]
}
new_X = pd.DataFrame.from_dict(test)


########## TESTS ##########
if __name__ == '__main__':
    # death_train()
    # print(death_pred(new_X))
    pass
