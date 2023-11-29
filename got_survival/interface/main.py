from got_survival.ml_logic.model_death_prediction import death_read_data, death_x_and_y, death_create_pipeline, death_split_train, death_train_model, death_cross_validate_result, death_prediction
#from got_survival.ml_logic.model_episode_of_death import episode_read_data, episode_x_and_y, episode_create_pipeline, episode_split_train, episode_model, episode_cross_validate_result, episode_prediction
#from sklearn.linear_model import LogisticRegression
import pickle

def death_train():
    X, y = death_x_and_y()
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    pipe = death_create_pipeline()
    pipe.fit(X_train, y_train.values.ravel())

    # we should save the model somewhere instead of returning it
    with open("got_survival/models_pickle/pipe.pkl", "wb") as file:
        pickle.dump(pipe, file)


def death_evaluate():
    # if we save the model somewhere, we should load it instead of passing it to the function
    pipe = pickle.load(open("got_survival/models_pickle/pipe.pkl", "rb"))
    X, y = death_x_and_y()
    X_train, X_test, y_train, y_test = death_split_train(X, y)
    score = pipe.score(X_test, y_test)
    # maybe save the score somewhere?
    return score


print(death_evaluate())
