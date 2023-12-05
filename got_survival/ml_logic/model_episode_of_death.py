import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import ColumnTransformer
from xgboost import XGBClassifier

def episode_x_and_y() -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Reads the data, filters it to only be the people who die and splits it into X and y
    '''
    df = pd.read_csv("processed_data/cleaned_data_final.csv")
    df.drop(columns=['name', 'episode', 'deaths'], axis=1, inplace=True)
    df = df[df['isAlive'] == 0].drop(columns="isAlive")

    df['season_half'] = np.where((df['season'] >= 0) & (df['season'] <= 4), 1, 0)
    X = df.drop(columns = ["episode_num", "season", "season_half"], axis=1)
    y = df[["season_half"]]
    return X, y

def episode_create_pipeline() -> Pipeline:
    '''
    Creates XGBClassifier pipeline
    '''
    cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer([
        ('cat_transformer', cat_transformer, ['origin'])],
        remainder='passthrough'
    )
    return make_pipeline(preprocessor, XGBClassifier(max_depth = 3, n_estimators = 385,
                                                     learning_rate = 0.9733781714200092))

def episode_split_train(
        X: pd.DataFrame,
        y: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
    Creates train-test-split with random state
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3)
    return X_train, X_test, y_train, y_test

def episode_cross_validate_result(
        pipe:Pipeline,
        X_train:pd.DataFrame,
        y_train:pd.DataFrame
    ) -> float:
    '''
    Cross validates a given XGBClassifier regression pipeline
    '''
    cv_results = cross_validate(pipe, X_train, y_train, cv=5, scoring="macro_f1")
    return cv_results["test_score"].mean()
