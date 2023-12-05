import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score

def death_x_and_y() -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Reads the data and splits it into X and y
    '''
    df = pd.read_csv("processed_data/cleaned_data_final.csv")
    X = df.drop(columns = ["name",'isAlive','episode','deaths',"season","episode_num"], axis=1)
    y = df[["isAlive"]]
    return X, y

def death_create_pipeline() -> Pipeline:
    '''
    Creates logistic regression pipeline
    '''
    num_transformer = Pipeline([('robust_scaler', RobustScaler())])

    cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer([
        ('num_transformer', num_transformer, ["isMarried","isNoble","male","popularity"]),
        ('cat_transformer', cat_transformer, ['origin'])
    ])

    return make_pipeline(preprocessor, LogisticRegression())

def death_split_train(
        X:pd.DataFrame,
        y:pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
    Creates train-test-split with random state
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3, stratify=y)

    return X_train, X_test, y_train, y_test

def death_cross_validate_result(
        pipe:Pipeline,
        X_train:pd.DataFrame,
        y_train:pd.DataFrame
    ) -> float:
    '''
    Cross validates a given logistic regression pipeline
    '''
    cv_results = cross_validate(pipe, X_train, y_train, cv=5, scoring="f1")
    return cv_results["test_score"].mean()

def death_f1_score(
        y_true:pd.DataFrame,
        y_pred:pd.Series
    ) -> float:
    '''
    Calculates f1 score for prediction and true values
    '''
    return f1_score(y_true, y_pred)
