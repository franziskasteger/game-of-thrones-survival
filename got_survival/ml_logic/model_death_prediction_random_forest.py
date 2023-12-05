import pandas as pd
from sklearn.model_selection import cross_validate
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score, classification_report

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



def death_cross_validate_result_rf(
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
    print(f'Score to return is f1_macro: {cv_results["f1_macro"].mean()}')
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
    print(f"Returns f1_macro: {f1_score(y_true, y_pred, average='macro')}")
    return f1_score(y_true, y_pred, average='macro')
