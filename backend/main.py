import pickle
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

model=pickle.load(open("model.pkl", "rb"))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class InputData(BaseModel):
    Age:int
    Gender:str
    Policy_Type:object
    Vehicle_Type:object
    Accident_Type:object
    Annual_Premium:int
    Claim_Amount:int
    Police_Report:object
    Witness_Present:object
    Past_Claims:int
    Days_To_Claim:int
    Incident_Location:object	

def predict(data):
    return model.predict([data])


@app.get("/")
def home():
    return {"message": "ML API is running"}


@app.post("/predict")
def predict(data: InputData):
    try:
        input_dict = {
            "Age": [data.Age],
            "Gender": [data.Gender],
            "Policy_Type": [data.Policy_Type],
            "Vehicle_Type": [data.Vehicle_Type],
            "Accident_Type": [data.Accident_Type],
            "Annual_Premium": [data.Annual_Premium],
            "Claim_Amount": [data.Claim_Amount],
            "Police_Report": [data.Police_Report],
            "Witness_Present": [data.Witness_Present],
            "Past_Claims": [data.Past_Claims],
            "Days_To_Claim": [data.Days_To_Claim],
            "Incident_Location": [data.Incident_Location]
        }

        # ── Step 2: Convert to DataFrame ──────────────────────
        input_df = pd.DataFrame(input_dict)          # ✅ was missing

        # ── Step 3: Define categorical columns ────────────────
        categorical_cols = [
            "Gender",
            "Policy_Type",
            "Vehicle_Type",
            "Accident_Type",
            "Police_Report",
            "Witness_Present",
            "Incident_Location"
        ]

        # ── Step 4: Encode categorical columns ────────────────
        input_df[categorical_cols] = scaler.transform(input_df[categorical_cols])

        # ── Step 5: Predict ───────────────────────────────────
        prediction = model.predict(input_df)

        pred = int(prediction[0])
        
        if pred == 1:
           result = 'you get insurance'
        else: 
           result = 'yor dont get insurance'
        
        return {'prediction':result}
    
    except Exception as e:
        return {"error": str(e)}

