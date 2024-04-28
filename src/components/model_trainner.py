import os
import sys

from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import AdaBoostRegressor,GradientBoostingRegressor,RandomForestRegressor

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRFRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')
    
class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("spliting training and test input data")
            x_train,y_train,x_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors " : KNeighborsRegressor(),
                "XGB Regressor": XGBRFRegressor(),
                "Catboosting Regressor": CatBoostRegressor(),
                "AdaBoost regreesor": AdaBoostRegressor()
            }
            logging.info('model evaluation started')
            model_report:dict = evaluate_models(X_train = x_train,Y_train=y_train,
                                                X_test = x_test,Y_test = y_test,
                                                models = models)
            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            
            best_model  = models[best_model_name]
            
            if best_model_score < 0.6:
                logging.error('No best model found')
                raise CustomException ("No best model found")
            logging.info("Best model selected "+ best_model_name)
            
            save_object(file_path=self.model_trainer_config.trained_model_file_path
                        ,obj= best_model)
            predicted = best_model.predict(x_test)
            r2_square = r2_score(y_test,predicted)
            return r2_square,best_model_name
            
        except Exception as e:
            logging.error(e)
            raise CustomException(e)

