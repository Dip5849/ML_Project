import sys
from fastapi import FastAPI

from src.pipeline.schema import student_info, prediction
from src.pipeline.prediction import PredictionPipeline
from src.exception import CustomException

app = FastAPI()



@app.post("/predict",response_model=prediction)

def predict(data:student_info):
    try:
        pred = PredictionPipeline.predict(data=data)
        return {'prediction':float(pred)}
    except Exception as e:
        raise CustomException(e,sys)