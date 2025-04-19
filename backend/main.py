from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from budgeting_advisor import router as advisor_router
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(advisor_router)


# Load model and data
model = joblib.load("models/income_predictor_model.joblib")
user_profiles = pd.read_csv("data/user_profiles.csv")
income_df = pd.read_csv("data/income_history.csv")

class UserRequest(BaseModel):
    username: str


@app.post("/predict_income")
def predict_income(request: UserRequest):
    username = request.username

    # Validate user
    if username not in user_profiles["username"].values:
        raise HTTPException(status_code=404, detail="User not found")

    # Get user profile
    user_profile = user_profiles[user_profiles["username"] == username].iloc[0]
    job_type = user_profile["job_type"]
    tier = user_profile["tier"]

    # Get income history
    user_income = income_df[income_df["username"] == username]
    if user_income.empty:
        raise HTTPException(status_code=404, detail="No income history found for user")

    month_1 = user_income["month_1"].values[0]
    month_2 = user_income["month_2"].values[0]
    month_3 = user_income["month_3"].values[0]

    input_data = pd.DataFrame([{
        "job_type": job_type,
        "tier": tier,
        "month_1": month_1,
        "month_2": month_2,
        "month_3": month_3
    }])

    prediction = model.predict(input_data)[0]
    volatility = abs(month_3 - prediction) / month_3

    return {
        "predicted_income": round(prediction, 2),
        "volatility_estimate": round(volatility, 2)
    }


