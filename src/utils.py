import os
import sys

import numpy as np
import pandas as pd
import dill
from src.logger import logging

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
        