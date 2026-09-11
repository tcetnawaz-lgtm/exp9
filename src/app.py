import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Define the expected JSON payload
class NetworkTraffic(BaseModel):
    bytes_per_packet: float
    connection_duration_ms: float
    failed_logins: float

app = FastAPI(title="Network Intrusion Detection API")
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load("models/intrusion_model.pkl")
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")

@app.get("/health")
def health_check():
    """Jenkins uses this to verify the container is running."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy"}

@app.post("/predict")
def predict_traffic(data: NetworkTraffic):
    """Predicts if network traffic is normal or an intrusion."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)[0]
    
    return {
        "status": "Malicious Intrusion Detected!" if prediction == 1 else "Normal Traffic",
        "threat_level": int(prediction)
    }