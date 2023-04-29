#!/usr/bin/python

import numpy as np
import xgboost as xgb
from sklearn.datasets import make_classification
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.utils import class_weight
from sklearn import preprocessing
import time
import sys
import pandas as pd
import os
# Modelado
# ==============================================================================
from sklearn.neural_network import MLPRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_selector
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import KFold
from sklearn import set_config
import multiprocessing
from joblib import dump, load



def predict_price(Year,Mileage,State,Make, Model):

    url_ = pd.DataFrame([Year,Mileage,State,Make, Model], index=['Year','Mileage','State','Make', 'Model']).T
        
    categoricas = ['State','Make','Model']
    numericas = ['Year','Mileage']
    
    
    X_var_numericas = url_[numericas]
    X_std_scaller = load(os.path.dirname(__file__) + '/std_scaler.bin')
    X_Train_StdSca = X_std_scaller.fit_transform(X_var_numericas)
    
    ## Estandarizar categoricas
    
    X_var_categoricas = url_[categoricas]
    enc = load('one_hot_scaller.bin')
    X_train_OneHot = enc.transform(X_var_categoricas)
    
    ## Matrices X de entrenamiento y prueba
    X_Train = np.hstack([X_Train_StdSca,X_train_OneHot])
    
    model = load('best_model_price_cars.bin')
    p1 = model.predict(X_Train)

    return p1[0]


if __name__ == "__main__":
    
    if len(sys.argv) <= 4:
        print("Please add all fields: 'Year','Mileage','State','Make', 'Model'")
        
    else:

        Year = int(sys.argv[1])
        Mileage = int(sys.argv[2])
        State = sys.argv[3]
        Make = sys.argv[4]
        Model = sys.argv[5]
        p1 = predict_price(Year,Mileage,State,Make, Model)
        
        print(f"{Year},{Mileage},{State},{Make}, {Model}")
        print('Precio estimado: ', p1)
        