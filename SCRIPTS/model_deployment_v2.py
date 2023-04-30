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
import json
import re

# 2017 9913 FL Jeep 

#Year = 2017
#Mileage = 9913
#State = 'FL'
#Make = 'Jeep'
#Model = 'Wrangler'
#os.getcwd()

def  extraer_lineas(modelo_veh):
    patron_version = re.compile("[A-Z]{2,}")
    extraccion = re.findall(patron_version,modelo_veh)

    if len(extraccion)>0:
        extraccion = extraccion[0]
    else:
        patron_4puerta = re.compile("4dr$")
        extraccion = re.findall(patron_4puerta,modelo_veh)
        
        if len(extraccion)>0:
            extraccion = '4doors'
        else:
            extraccion = 'No_version'

    return extraccion


def transformar(Year,Mileage,State,Make, Model):
    X = pd.DataFrame([Year,Mileage,State,Make, Model], index=['Year','Mileage','State','Make', 'Model']).T    
    mx_year = 2018

    encoder_model = load( '../OUTPUT/onehot_model_variables_model_1.bin')
    encoder_variables = load( '../OUTPUT/onehot_encoder_variables_model_1.bin')

    with open('../OUTPUT/dict_maker.json', 'r') as f:
        dict_maker = json.load(f)
    
    with open('../OUTPUT/dict_models.json', 'r') as f:
        dict_models = json.load(f)
        
    X["cluster_make"] = X["Make"].map(dict_maker).fillna(-1)
    X["cluster_model"] = X["Model"].map(dict_models).fillna(-1)
    #X["Mileage"] = np.log(X.loc[0,"Mileage"])
    X["Year"] = X["Year"].astype(int)
    X["Age"] = int(mx_year - X["Year"])
    X["Version"] = X["Model"].apply(extraer_lineas)
    

    col_dummies = ['Make','State','cluster_make','cluster_model','Version']

    encoder = encoder_variables

    X = pd.concat([X,pd.DataFrame(encoder.transform(X[col_dummies]).toarray(), columns = encoder.get_feature_names_out(), index = X.index)], axis = 1)
    X = X.drop(columns=col_dummies)


    X = pd.concat([X,pd.DataFrame(encoder_model.transform(X[["Model"]]).toarray(), columns = encoder_model.get_feature_names_out(), index = X.index)], axis = 1)
    X = X.drop(columns="Model")

    return X


def predict_price(Year,Mileage,State,Make, Model):
    
    X_test_transformed = transformar(Year,Mileage,State,Make, Model)
    stk = load('../OUTPUT/bgr_model_2.bin')
    y_pred = stk.predict(X_test_transformed)
    #y_pred = np.exp(y_pred)*1000
    
    return y_pred 


if __name__ == "__main__":
    
    if len(sys.argv) <= 4:
        print("Please add all fields: 'Year','Mileage','State','Make', 'Model'")
        
    else:

        Year = int(sys.argv[1])
        Mileage = np.log(int(sys.argv[2]))
        State = sys.argv[3]
        Make = sys.argv[4]
        Model = sys.argv[5]
        p1 = predict_price(Year,Mileage,State,Make, Model)
        
        print(f"{Year},{Mileage},{State},{Make}, {Model}")
        print('Precio estimado: ', p1)
        
        
        
