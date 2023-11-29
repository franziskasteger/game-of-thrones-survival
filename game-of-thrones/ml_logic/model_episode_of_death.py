import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import learning_curve
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from scipy import stats
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

#Reading CSV file
def episode_read_data():
    df = pd.read_csv("raw_data/20231128_only_deaths_ep_weights.csv")
    return df

def episode_x_and_y():
    df = episode_read_data()
    X = df
    X = X.drop(columns = ["Unnamed: 0","name",'isAlive'], axis=1)
    y = df["episode_global_num"]
    y = y.to_frame(name="episode_global_num")
    return X, y

#Preprocessing
def episode_create_pipeline():
    num_transformer = Pipeline([('standard_scaler', StandardScaler())])

    cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer([
        ('num_transformer', num_transformer, ["weights_simple"]),
        ('cat_transformer', cat_transformer, ['allegiance','killer','killers_house','location','method'])
    ])
    return preprocessor

#Splitting Data
def episode_split_train():
    X, y = episode_x_and_y()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3)

    X_train_processed = pd.DataFrame(episode_create_pipeline().fit_transform(X_train),columns=episode_create_pipeline().get_feature_names_out())
    return X_train_processed, X_test, y_train, y_test

#CreateModel
def episode_model():
    model = LinearRegression()
    return model

#Cross Validate Model
def episode_cross_validate_result():
    X_train_processed, X_test, y_train, y_test = episode_split_train()
    model = LinearRegression()
    cv_results = cross_validate(model, X_train_processed, y_train, cv=5)
    test = cv_results["test_score"].mean()
    return test

#Predict Y
def episode_prediction(X_train_processed):
    y_pred = model().predict(X_train_processed)
    return y_pred
