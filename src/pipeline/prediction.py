import sys
import numpy as np
import pandas as pd
from src.exception import CustomException
from src.utils import load_obj


class PredictionPipeline:

    def __init__(self):
        pass

    def predict(data):
        try:

            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'
            model= load_obj(model_path)
            preprocessor = load_obj(preprocessor_path)
            input_df = pd.DataFrame([{
                "writing_score": data.writing_score,
                "reading_score": data.reading_score,
                "gender": data.gender,
                "race_ethnicity": data.race_ethnicity,
                "parental_level_of_education": data.parental_level_of_education,
                "lunch": data.lunch,
                "test_preparation_course": data.test_preparation_course,
                
                
            }])
            data_arr = preprocessor.transform(input_df)
            pred = model.predict(data_arr)

            return pred


        except Exception as e:
            raise CustomException(e,sys)


    