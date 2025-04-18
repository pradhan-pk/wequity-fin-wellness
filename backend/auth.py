from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd

router = APIRouter()

# Sample users — in real app, use a database
USER_DATA = pd.DataFrame([
    {"username": "avinya", "password": "admin"},
    {"username": "bivas", "password": "admin"},
])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(req: LoginRequest):
    user = USER_DATA[
        (USER_DATA["username"] == req.username) &
        (USER_DATA["password"] == req.password)
    ]
    if user.empty:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "username": req.username}
