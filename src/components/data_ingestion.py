import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTranasformation,DataTransformationConfig

@dataclass
class DataIngestionConfig:
    train_data_path:str =  os.path.join("artifacts","train.csv")
    test_data_path:str =  os.path.join("artifacts","test.csv")
    raw_data_path:str = os.path.join("artifacts","raw.csv")

class DataIngestion:
    
    def __init__(self) -> None:
        logging.info('Reading Data configuration')
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        logging.info("Data Ingestion initiated")
        try:
            df = pd.read_csv('notebooks\data\stud.csv')
            logging.info("Read the original data as dataframe")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False, header=True)
            logging.info(f'Raw Csv saved at {self.ingestion_config.raw_data_path}')
            
            logging.info('Train test split Initiated')
            train_set,test_set = train_test_split(df,test_size=.25,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False, header=True)
            logging.info(f"Train and Test set saved at {self.ingestion_config.train_data_path} and {self.ingestion_config.test_data_path}")
            logging.info('Ingestion successfull')
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.error('Data Ingestion Failed')
            raise CustomException(e)
          
            
            
if __name__ == "__main__":
    logging.info("Starting Data Ingestion")
    obj = DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()
    
    logging.info('Starting Data Transformation')
    data_transformation = DataTranasformation()
    data_transformation.initiate_data_transformation(train_data_path,test_data_path)
    
    