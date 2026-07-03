from gemini_helper import get_ai_response

prompt = """
Suggest 3 gaming laptops under ₹1 lakh.
Include brand names and one-line features.
"""

response = get_ai_response(prompt)

print(response)