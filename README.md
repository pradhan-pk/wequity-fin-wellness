# Gig Workers' Financial Wellness App


## Features
- Income prediction using ML model trained on synthetic Indian gig workers data
- Volatility estimation based on historical income
- Budgeting advisor and financial coach using opensource Mistral model


## Setup
```bash
git clone <repo>
cd financial-wellness-app
```

Get your hugging face token.
Get access to mistralai/Mistral-Small-3.1-24B-Instruct-2503 on Hugging Face
Create a .env file in base directory and add inside it - 
HF_TOKEN=<your_huggingface_token>


- Frontend: http://localhost:8501
- Backend API: http://localhost:8000/



## FastAPI backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app
```


## Streamlit Frontend

```bash
cd streamlit_frontend
pip install -r requirements.txt
streamlit run app.py
```




