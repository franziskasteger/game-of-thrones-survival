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
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import warnings

#Reading CSV file
df = pd.read_csv("processed_data/data_cleaned_Carmen/20231128_char_pred_isAlive_updated.csv")

X = df
X = X.drop(columns = ["Unnamed: 0","name",'isAlive'], axis=1)

y = df["isAlive"]
y = y.to_frame(name="isAlive")


#Preprocessing
num_transformer = Pipeline([('robust_scaler', RobustScaler())])

cat_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=False)

preprocessor = ColumnTransformer([
    ('num_transformer', num_transformer, ["numDeadRelations","popularity"]),
    ('cat_transformer', cat_transformer, ['house'])
])

#Splitting Data
def split_train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=3, stratify=y)

    X_train_processed = pd.DataFrame(preprocessor.fit_transform(X_train),columns=preprocessor.get_feature_names_out())
    return X_train_processed, X_test, y_train, y_test

#Cross Validate Model
def cross_validate(X_train_processed, y_train):
    model = LogisticRegression()
    cv_results = cross_validate(model, X_train, y_train, cv=5)
    test = cv_results["test_score"].mean()
    return test

#Predict Y
def prediction(X_train_processed_
    y_pred = model.predict(X_train_processed)
    return y_pred

#Grid Search CV
grid = {'l1_ratio': [0.2, 0.5, 0.8]}

search = GridSearchCV(
    model,
    grid, 
    scoring = 'accuracy',
    cv = 5,
    n_jobs=-1)

search.fit(X_train, y_train)

# Best score
print(search.best_score_)

# Best Params
search.best_params_

# Best estimator
search.best_estimator_

#Random Search
grid = {'l1_ratio': stats.uniform(0, 1)}

search = RandomizedSearchCV(
    model,
    grid, 
    scoring='accuracy',
    n_iter=100,
    cv=5, n_jobs=-1
)

search.fit(X_train, y_train)
search.best_estimator_
print(search.best_score_)

#Preprocessing X
X = pd.DataFrame(preprocessor.fit_transform(X),
            columns=preprocessor.get_feature_names_out())

#Learning Curve
train_sizes = [25,50,75,100,250,500,750,1000,1150]

train_sizes, train_scores, test_scores = learning_curve(
    estimator=LogisticRegression(), X=X, y=y, train_sizes=train_sizes, cv=5)

train_scores_mean = np.mean(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)

plt.plot(train_sizes, train_scores_mean, label = 'Training score')
plt.plot(train_sizes, test_scores_mean, label = 'Test score')
plt.ylabel('accuracy', fontsize = 14)
plt.xlabel('Training set size', fontsize = 14)
plt.title('Learning curves', fontsize = 18, y = 1.03)
plt.legend()
