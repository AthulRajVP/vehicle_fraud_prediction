import pickle
import pandas as pd
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load model from the same directory as this script
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")
model = pickle.load(open(model_path, 'rb'))

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
        print(f"📨 Received data: {data}")
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

        # ── Step 3: Predict ──────────────────────────────────
        print(f"📊 DataFrame: {input_df}")
        prediction = model.predict(input_df)
        print(f"🎯 Prediction: {prediction}")

        pred = int(prediction[0])
        
        if pred == 1:
           result = 'you get insurance'
        else: 
           result = 'yor dont get insurance'
        
        return {'prediction':result}
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

