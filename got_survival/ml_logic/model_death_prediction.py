import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from scipy import stats
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score

#Reading CSV file
def death_read_data():
    df = pd.read_csv("processed_data/cleaned_data_final.csv")
    return df

def death_x_and_y():
    df = death_read_data()
    X = df
    X = X.drop(columns = ["Unnamed: 0","name",'isAlive','episode','deaths',"season","episode_num"], axis=1)
    y = df["isAlive"]
    y = y.to_frame(name="isAlive")
    return X, y

#Preprocessing
def death_create_pipeline():
    num_transformer = Pipeline([('robust_scaler', RobustScaler())])

    cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

    preprocessor = ColumnTransformer([
        ('num_transformer', num_transformer, ["isMarried","isNoble","male","popularity"]),
        ('cat_transformer', cat_transformer, ['origin'])
    ])

    return make_pipeline(preprocessor, LogisticRegression())

#Splitting Data
def death_split_train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3, stratify=y)
    # transformer = death_create_pipeline()
    # X_train_processed = pd.DataFrame(transformer.fit_transform(X_train),columns=transformer.get_feature_names_out())
    # X_test_processed = pd.DataFrame(transformer.transform(X_test),columns=transformer.get_feature_names_out())
    return X_train, X_test, y_train, y_test

#Cross Validate Model
def death_cross_validate_result(model, X_train_processed, y_train):
    cv_results = cross_validate(model, X_train_processed, y_train, cv=5, scoring="f1")
    test = cv_results["test_score"].mean()
    return test

def death_f1_score(y_true, y_pred):
    return f1_score(y_true, y_pred)


#Predict Y
def death_prediction(model , X):
    y_pred = model.predict(X)
    return y_pred


#CreateModel
def death_train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model


#Grid Search CV
# grid = {'l1_ratio': [0.2, 0.5, 0.8]}
#
# search = GridSearchCV(
#     model,
#     grid,
#     scoring = 'accuracy',
#     cv = 5,
#     n_jobs=-1)

# search.fit(X_train, y_train)

# Best score
# # print(search.best_score_)

# Best Params
# search.best_params_

# Best estimator
# search.best_estimator_

#Random Search
# grid = {'l1_ratio': stats.uniform(0, 1)}
#
# search = RandomizedSearchCV(
#     model,
#     grid,
#     scoring='accuracy',
#     n_iter=100,
#     cv=5, n_jobs=-1
# )
#
# search.fit(X_train, y_train)
# search.best_estimator_
# print(search.best_score_)

#Preprocessing X
# X = pd.DataFrame(preprocessor.fit_transform(X),
#             columns=preprocessor.get_feature_names_out())

#Learning Curve
# train_sizes = [25,50,75,100,250,500,750,1000,1150]
#
# train_sizes, train_scores, test_scores = learning_curve(
#     estimator=LogisticRegression(), X=X, y=y, train_sizes=train_sizes, cv=5)
#
# train_scores_mean = np.mean(train_scores, axis=1)
# test_scores_mean = np.mean(test_scores, axis=1)
#
# plt.plot(train_sizes, train_scores_mean, label = 'Training score')
# plt.plot(train_sizes, test_scores_mean, label = 'Test score')
# plt.ylabel('accuracy', fontsize = 14)
# plt.xlabel('Training set size', fontsize = 14)
# plt.title('Learning curves', fontsize = 18, y = 1.03)
# plt.legend()
