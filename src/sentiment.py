import os
import requests
from dotenv import load_dotenv

# First line loads the .env file. Second line fetches the file and stores the secret API token from .env file (excluded from GitHub via .gitignore).
load_dotenv()
api_token = os.getenv("HF_TOKEN")

# Hugging Face Inference API endpoint for tabularisai sentiment analysis model.
API_URL = "https://router.huggingface.co/hf-inference/models/tabularisai/robust-sentiment-analysis"

headers = {
    "Authorization" : "Bearer " + api_token
}

def analyze_sentiment(text):
    """
    This function analyzes the sentiment of text using the HF API.
    
    - text: the input we want to analyze
    - payload: packages the text into a format HF understands
    - requests.post: sends the package to HF along with our headers
    - response: where the result from HF lands after analysis
    """
    payload = {
        "inputs" : text
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()
