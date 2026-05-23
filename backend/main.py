import pickle
import pandas as pd
import numpy as np
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")
model = pickle.load(open(model_path, 'rb'))

scaler_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scaler.pkl")
scaler = pickle.load(open(scaler_path, 'rb'))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    Age: int
    Gender: str
    Policy_Type: str
    Vehicle_Type: str
    Accident_Type: str
    Annual_Premium: float
    Claim_Amount: float
    Police_Report: str
    Witness_Present: str
    Past_Claims: int
    Days_To_Claim: int
    Incident_Location: str

@app.get("/")
def home():
    return {"message": "ML API is running"}

@app.post("/predict")
def predict(data: InputData):
    try:
        raw = {
            "Age": data.Age,
            "Annual_Premium": data.Annual_Premium,
            "Claim_Amount": data.Claim_Amount,
            "Past_Claims": data.Past_Claims,
            "Days_To_Claim": data.Days_To_Claim,
            "Gender": data.Gender,
            "Policy_Type": data.Policy_Type,
            "Vehicle_Type": data.Vehicle_Type,
            "Accident_Type": data.Accident_Type,
            "Police_Report": data.Police_Report,
            "Witness_Present": data.Witness_Present,
            "Incident_Location": data.Incident_Location,
        }

        df_input = pd.DataFrame([raw])

        # Same get_dummies as training
        df_input = pd.get_dummies(
            df_input,
            columns=['Gender', 'Policy_Type', 'Vehicle_Type',
                     'Accident_Type', 'Police_Report', 'Witness_Present',
                     'Incident_Location'],
            drop_first=True,
            dtype=int
        )

        # ✅ Exact 16 columns the model was trained on
        # (matches your notebook: drop_first=True on your dataset)
        trained_columns = [
            'Age', 'Annual_Premium', 'Claim_Amount', 'Past_Claims', 'Days_To_Claim',
            'Gender_Male',
            'Policy_Type_Liability', 'Policy_Type_Premium',
            'Vehicle_Type_SUV', 'Vehicle_Type_Sedan', 'Vehicle_Type_Truck',
            'Accident_Type_Rear-End', 'Accident_Type_Theft',
            'Police_Report_Yes',
            'Witness_Present_Yes',
            'Incident_Location_Suburban'
        ]

        # Add any missing columns with 0
        for col in trained_columns:
            if col not in df_input.columns:
                df_input[col] = 0

        # Keep only the 16 trained columns in exact order
        df_input = df_input[trained_columns]

        # Scale exactly like training
        df_scaled = scaler.transform(df_input)

        prediction = model.predict(df_scaled)
        pred = int(prediction[0])

        result = 'You get insurance ✅' if pred == 1 else "You don't get insurance ❌"
        return {'prediction': result}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}