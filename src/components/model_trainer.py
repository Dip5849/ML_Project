import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utils import save_obj, evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')

    models = {
        'Random forest': RandomForestRegressor(),
        "Decision Tree": DecisionTreeRegressor(),
        "Gradient Boosting": GradientBoostingRegressor(),
        "Linear Regression": LinearRegression(),
        "K-Neighbour Regressor": KNeighborsRegressor(),
        "XGBRegressor": XGBRegressor(),
        "CatBoosting Regressor": CatBoostRegressor(verbose=False,allow_writing_files=False),
        "AdaBoost Regressor": AdaBoostRegressor()
    }

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Started spliting train and test data")
            x_train,y_train,x_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            model_report:dict = evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=self.model_trainer_config.models)
            logging.info("Got model performance report")

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = self.model_trainer_config.models[best_model_name]
            
            if best_model_score<0.6:
                logging.error(f"Couldn't find a best model for both train and test dataset")
                raise CustomException("No best model found",sys)

            logging.info('Got best model for both train and testing dataset')
            
            save_obj(file_path=self.model_trainer_config.trained_model_file_path,obj=best_model)

            predict = best_model.predict(x_test)
            return r2_score(predict,y_test), best_model_name
        
        except Exception as e:
            raise CustomException(e,sys)