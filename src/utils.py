import os
import sys

import numpy as np
import pandas as pd
import dill
from src.logger import logging
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomException

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as object_file:
            dill.dump(obj,object_file)
            
    except Exception as e:
        logging.ERROR(e)
        raise CustomException(e)
    
def load_object(file_pkl):
    try:
        with open(file_pkl,'rb' ) as file_object:
            return dill.load(file_object)
    except Exception as e:
        logging.error('Fail to load object')
        raise CustomException(e)
        
        
        
        
def evaluate_models(X_train,Y_train,X_test,Y_test,models,params):
    try:
        report = dict()
        for i in range(len(list(models))):
            
            model = list(models.values())[i]
            para=params[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,Y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,Y_train)

            
            model = list(models.values())[i]
            model.fit(X_train,Y_train)
            
            
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            train_model_score = r2_score(Y_train,y_train_pred)
            test_model_score = r2_score(Y_test,y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
            return report
        
    except Exception as e:
        
        logging.error(e)
        raise CustomException(e)
    