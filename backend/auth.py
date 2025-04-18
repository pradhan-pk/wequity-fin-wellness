from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd

router = APIRouter()

# # Sample users — in real app, use a database
# USER_DATA = pd.DataFrame([
#     {"username": "avinya", "password": "admin"},
#     {"username": "bivas", "password": "admin"},
#     {"username": "user1", "password": "pass1"},
# ])

class LoginRequest(BaseModel):
    username: str
    password: str

USER_DATA = pd.read_csv(r"data\user_profiles.csv")
user_profiles = USER_DATA


@router.post("/login")
def login(req: LoginRequest):
    user = USER_DATA[
        (USER_DATA["username"] == req.username) &
        (USER_DATA["password"] == req.password)
    ]
    if user.empty:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
         user_profile = user_profiles[user_profiles["username"] == req.username].iloc[0]
         print(user_profile)

    return {"message": "Login successful", 
            "username": req.username, 
            "city": user_profile["city"], 
            "city_tier": user_profile["tier"],
            "job_type": user_profile["job_type"]}


