import os
import sys
import dill

import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging
from sklearn.metrics import r2_score



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



def evaluate_models(x_train,y_train,x_test,y_test,models):
    try:
        report = {}

        for i in range(len(models)):
            model = list(models.values())[i]

            model.fit(x_train,y_train)
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            train_score = r2_score(y_train,y_train_pred)
            test_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_score

        return report
    except Exception as e:
        raise CustomException(e,sys)
        

def load_obj(file_path):
    try:
        with open(file_path,'rb') as file:
            return dill.load(file)
    except Exception as e:
        raise CustomException(e,sys)
