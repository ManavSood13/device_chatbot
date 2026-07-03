import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# API key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_response(user_message):
    try:
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        raise