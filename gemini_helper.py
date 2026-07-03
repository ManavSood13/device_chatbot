import google.generativeai as genai
import os

# Paste your API key here
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