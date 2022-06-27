import pandas as pd
import sqlite3
import os
from sklearn.ensemble import RandomForestRegressor
from category_encoders import TargetEncoder
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform
import pickle
import pdb
import warnings
warnings.filterwarnings('ignore')


DB_FILENAME = "mosquito_db.sqlite3"
DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
conn = sqlite3.connect(DB_FILEPATH)
cur = conn.cursor()

df = pd.read_sql('select * from mosquito', con =conn)
df = df.drop('Id', axis= 1)
target = '모기지수'
X_train = df.drop(columns = target)
y_train = df[target]


pipe = make_pipeline(
    TargetEncoder(),
    RandomForestRegressor(n_estimators=100, random_state=42)
)
dists = {
    'targetencoder__smoothing': [2.,20.,50.,100.,500.,1000.], # int로 넣으면 error(bug)
    'targetencoder__min_samples_leaf': randint(1, 10),     
    'randomforestregressor__n_estimators': randint(100, 500), 
    'randomforestregressor__max_depth': [5, 10, 13 ,15, 17, 20, 25], 
    'randomforestregressor__min_samples_leaf' : [1,3,6],
    'randomforestregressor__max_leaf_nodes' : [300, 600, 1000],
    'randomforestregressor__max_features': ['sqrt', 'log2', None, 'auto'], # max_features
}
clf = RandomizedSearchCV(
    pipe, 
    param_distributions=dists, 
    n_iter=120, 
    cv=7, 
    scoring='f1',  
    verbose=1,
    n_jobs=-1
)

clf.fit(X_train, y_train)

with open('model.pkl','wb') as pickle_file:
    pickle.dump(clf, pickle_file)
