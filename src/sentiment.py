import os
import requests
from dotenv import load_dotenv

# First line loads the .env file. Second line fetches the file and stores the secret API token from .env file (excluded from GitHub via .gitignore).
load_dotenv()
api_token = os.getenv("HF_TOKEN")

# Hugging Face Inference API endpoint for tabularisai sentiment analysis model.
API_URL = "https://router.huggingface.co/hf-inference/models/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis"

headers = {
    "Authorization" : "Bearer " + api_token
}

def analyze_sentiment(text):
    payload = {
        "inputs" : text
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()
