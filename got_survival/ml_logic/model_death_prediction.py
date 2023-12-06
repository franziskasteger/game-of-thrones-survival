import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score, classification_report
from xgboost import XGBClassifier

def death_x_and_y() -> tuple[pd.DataFrame, pd.DataFrame]:
    '''
    Reads the data and splits it into X and y
    '''
    df = pd.read_csv("processed_data/cleaned_data_final.csv")
    X = df.drop(columns = ["name",'isAlive','episode','deaths',"season","episode_num"], axis=1)
    y = df[["isAlive"]]
    return X, y

## LOGISTIC REGRESSION PIPELINE
def death_create_pipeline(y:pd.DataFrame) -> Pipeline:
    '''
    Creates logistic regression pipeline
    '''
    num_transformer = Pipeline([('standar_scaler', StandardScaler())])

    cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer([
        ('num_transformer', num_transformer, ["popularity"]),
        ('cat_transformer', cat_transformer, ['origin']),
        ('passthrough', 'passthrough', ["isMarried","isNoble","male",])
    ])

    scale_pos_weights = len(y[y == 0]) / len(y[y == 1])
    xgb_model = XGBClassifier(
        scale_pos_weights=scale_pos_weights,
        learning_rate=0.024,
        n_estimators=200,
        max_depth=4,
        use_label_encode=False,
        eval_metric='logloss',
        min_child_weight=6,
        gamma=0.558
    )

    return make_pipeline(preprocessor, xgb_model)

## RANDOM FOREST PIPELINE
def death_create_pipeline_rf() -> Pipeline:
    '''
    Creates Random Forest regression pipeline
    '''
    cat_transformer = Pipeline(steps=[
    ('OHE', OneHotEncoder(handle_unknown='ignore',sparse_output=False))
    ])
    preprocessor = ColumnTransformer(
        transformers =[
            ('passthrough', 'passthrough', ["isMarried","isNoble","male","popularity"]),
            ('cat_transformer', cat_transformer, ['origin'])
    ])

    model_rf = RandomForestClassifier(n_estimators=282,
                                      max_depth=31,
                                      min_samples_leaf=12,
                                      class_weight='balanced')

    pipeline_rf = Pipeline([
        ('preprocessor', preprocessor),
        ('model_rf', model_rf)
    ])
    return pipeline_rf


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
    cv_results = cross_validate(pipe,
                                X_train,
                                y_train,
                                cv=5,
                                scoring=['accuracy', 'f1', 'roc_auc','recall','precision',"f1_macro"])
    print(f'----- Cross-validation Scores means -----')
    for i in cv_results:
        print(f' {i}: {cv_results[i].mean()}')
    print(f'-----------------------------------------')
    print(f'Function returns f1_macro score: {cv_results["f1_macro"].mean()}')
    return cv_results["f1_macro"].mean()


def death_f1_macro_score(
        y_true:pd.DataFrame,
        y_pred:pd.Series
    ) -> float:
    '''
    Calculates f1 macro-averaged score for prediction and true values
    '''
    print(f'----- classification_report -----')
    print(classification_report(y_true, y_pred))
    print(f'----------------------------------')
    print(f"Function returns f1_macro: {f1_score(y_true, y_pred, average='macro')}")

    return f1_score(y_true, y_pred, average='macro')


def death_f1_score(
        y_true:pd.DataFrame,
        y_pred:pd.Series
    ) -> float:
    '''
    Calculates f1 score for prediction and true values
    '''
    return f1_score(y_true, y_pred)
