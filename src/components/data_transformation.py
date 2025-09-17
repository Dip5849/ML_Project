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
from src.utils import save_obj


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_tranformation_config = DataTransformationConfig()

    def get_data_transformer_objects(self):
        logging.info("Data transformation initiated")
        try:
            numerical_columns = [
                'writing_score',
                'reading_score'
            ]
            categorical_columns = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            num_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')),
                    ('scaler',StandardScaler())
                ]
            )
            logging.info('Numerical columns scaling completed')
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),

                    ]
            )
            logging.info('Categorical columns encoding completed')

            preprocessor = ColumnTransformer(
                [
                    ('num_pipelines',num_pipeline,numerical_columns),
                    ('cat_pipelines',cat_pipeline,categorical_columns)
                ]
            )
            logging.info('All column transformation completed')

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df= pd.read_csv(train_path)
            test_df= pd.read_csv(test_path)
            logging.info('Readed the train and test set')

            logging.info('Obtaining processing object')
            preprocessing_obj = self.get_data_transformer_objects()


            target_column_name = 'math_score'

            input_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_train_df = train_df[target_column_name]
            logging.info('Splited train data into input and target')

            input_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_test_df = test_df[target_column_name]
            logging.info('Splited test data into input and target')

            logging.info('Appling preprocessing object to training and testing dataframe')
            input_train_arr = preprocessing_obj.fit_transform(input_train_df)
            input_test_arr = preprocessing_obj.transform(input_test_df)

            train_arr = np.c_[
                input_train_df,np.array(target_train_df)
            ]

            test_arr = np.c_[
                input_test_df,np.array(target_test_df)
            ]
            logging.info('Finished appling preprocessing object')

            save_obj(
                file_path = self.data_tranformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )
            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)