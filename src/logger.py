import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(),"logs")  # src// logs// files.log/ 
os.makedirs(logs_path,exist_ok=True)

LOG_FILES_PATH = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILES_PATH,
     format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
     level= logging.DEBUG # we use level info when we call it it will create logs
     
    )

if __name__ == "__main__":
   # Log messages of different levels
    logging.debug('This is test  debug message')  # Will  be logged 
    logging.info('This is test info message')   # Will  be logged 
    logging.warning('This is test warning message')      # Will be logged
    logging.error('This is an test error message')         # Will be logged
    logging.critical('This is test critical message')      # Will be logged
    
    
''' 
   When you set the logging level to X, Python will log messages that are at that level and higher.
   logging_levels = {
    "DEBUG": 10,
    "INFO": 20,
    "WARNING": 30,
    "ERROR": 40,
    "CRITICAL": 50
}

'''
    