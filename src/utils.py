import os
import sys
import dill

import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

def save_obj(file_path,obj):
    try:
        file_name = os.path.basename(file_path)
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path,'wb') as file:
            dill.dump(obj,file)
        logging.info(f"Saved the obj in {dir_path} as {file_name} file")
    except Exception as e:
        raise CustomException(e,sys)