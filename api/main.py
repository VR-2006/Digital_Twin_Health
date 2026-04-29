from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# -------------------------------
# FIX PATH (VERY IMPORTANT)
# -------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predictor import calculate_risk

app = FastAPI()


# -------------------------------
# INPUT SCHEMA
# -------------------------------
class PatientData(BaseModel):
    age: int
    sex: str
    resting_blood_pressure: int
    cholestoral: int
    Max_heart_rate: int


# -------------------------------
# API ROUTE
# -------------------------------
@app.post("/predict")
def predict(data: PatientData):

    input_data = {
        'age': data.age,
        'sex': data.sex,
        'chest_pain_type': 'Non-anginal Pain',
        'resting_blood_pressure': data.resting_blood_pressure,
        'cholestoral': data.cholestoral,
        'fasting_blood_sugar': 'No',
        'rest_ecg': 'Normal',
        'Max_heart_rate': data.Max_heart_rate,
        'exercise_induced_angina': 'No'
    }

    risk = calculate_risk(input_data)

    return {"risk": risk}