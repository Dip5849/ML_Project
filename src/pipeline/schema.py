import sys
from pydantic import BaseModel



class student_info(BaseModel):
    gender:str
    race_ethnicity:str
    parental_level_of_education:str
    lunch:str
    test_preparation_course:str
    reading_score:int
    writing_score:int

class prediction(BaseModel):
    prediction:float