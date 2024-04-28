import sys
import os

from dataclasses import dataclass
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

class DataTransformationConfig:
    preprocessor_object_file_path = os.path.join(
        'artifacts', "preprocessor.pkl")


class DataTranasformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """ This function is responsible for data transformation
        """
       
        
        try:
            numerical_features = [
                "writing_score", 'reading_score']
            categorical_features = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]
            logging.info('Preprocessing Pipline creation begian')

            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler(with_mean=False))
                ])
            logging.info("Numerical features Pipeline Created Successfully")

            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one hot encoder", OneHotEncoder()), # if sparce_output is not used, then use with_mean =False in all STandard scalars
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )
            logging.info(
                "Categorical features Pipline Created Successfully")

            preprocessor = ColumnTransformer(
                [
                    ("numerical_Pipeline", numerical_pipeline, numerical_features),
                    ("categorical_Pipeline", categorical_pipeline, categorical_features)
                ]
            )
            logging.info("Pipeline Created Successfully")
        except Exception as e:
            logging.error(e)
            raise CustomException(e)
        
        logging.info("returning preprocessor pipeline object")
        return preprocessor

    
    def initiate_data_transformation(self,train_set_path,test_set_path):
        try:
            train_df = pd.read_csv(train_set_path)
            test_df = pd.read_csv(test_set_path)
            logging.info('read train and test data completed')
            
            logging.info('Reading Preprocessor Pipeline object')
            preprocessing_obj = self.get_data_transformer_object()
            
            target_column_name = ['math_score']
            numerical_features = [
                "writing_score", 'reading_score']
            
            
            input_features_train_df = train_df.drop(columns=target_column_name)
            target_feature_train_df = train_df[target_column_name]
           
            
            input_features_test_df = test_df.drop(columns=target_column_name,axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info("Applying Preprocessor pipeline on train and test set")
            
      
            input_features_train_arrary = preprocessing_obj.fit_transform(input_features_train_df)

            input_features_test_array  = preprocessing_obj.transform(input_features_test_df)
            
            
            
            train_arr = np.c_[input_features_train_arrary,target_feature_train_df]
            test_arr = np.c_[input_features_test_array,target_feature_test_df]
            logging.info('Data Transformation successful')
            
            logging.info('Saving Preprocessor pkl')
            save_object(
                file_path = self.data_transformation_config.preprocessor_object_file_path,
                obj = preprocessing_obj
            )
            logging.info('Preprocessor pkl Saved successful')
            
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_object_file_path
            )
            

            
        except Exception as e:
            logging.error(e)
            raise CustomException(e)