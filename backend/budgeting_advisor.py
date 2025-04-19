from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from dotenv import load_dotenv, find_dotenv
import os
from huggingface_hub import InferenceClient

load_dotenv() 
hf_token = os.getenv("HF_TOKEN")
# print(hf_token)

router = APIRouter()

class Expenses(BaseModel):
    rent: int
    groceries: int
    utilities: int
    transport: int
    misc: int

class SuggestRequest(BaseModel):
    username: str
    city: str
    city_tier: str
    past_income: list[int]  # List of integers
    next_month_income: float
    volatility: float
    expenses: Expenses
    

@router.post("/save_expenses_suggest")
def save_expenses_suggest(req: SuggestRequest):
    
    prompt = f'''{req.username} is a gig worker in India working in {req.city} which is a {req.city_tier} city. His last 3 months' income is {str(req.past_income)}. His next month icome is predicted to be {req.next_month_income} with a volatility of {str(req.volatility)}. His monthly expenses are as follows: {str(req.expenses)}. 
          
    You are an expert financial wellness advisor. Based on {req.username}'s work profile, income and expenses, advise him on the budget and savings. Make sure your suggestion has atleast these 3 parts - save more on, consider investing in and cut back on.
    
    Be very specific and crisp - within 50 to 70 words. 
    
    '''

    client = InferenceClient(
        provider="nebius",
        api_key=hf_token,
    )

    completion = client.chat.completions.create(
        model="mistralai/Mistral-Small-3.1-24B-Instruct-2503",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        max_tokens=512,
    )

    
    return {"advice": completion.choices[0].message['content']}

    