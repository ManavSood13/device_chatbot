import requests
import json

# Your Watsonx Credentials
IBM_API_KEY = "xypQMF6Msyb0fnKU_g9hsPE_2_0bmjkt48Z4sm_Px-QL"
IBM_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-8b-instruct"
PROJECT_ID = "9958f02b-32a5-4e87-8b5e-3f3b45163c13"

def get_ai_response(user_message):
    # Step 1: Get Access Token
    auth_url = "https://iam.cloud.ibm.com/identity/token"
    auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    auth_data = f"apikey={IBM_API_KEY}&grant_type=urn:ibm:params:oauth:grant-type:apikey"

    auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_response.json()["access_token"]

    # Step 2: Query Watsonx Model
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model_id": MODEL_ID,
        "input": user_message,
        "project_id": PROJECT_ID,
        "parameters": {"max_new_tokens": 200}
    }

    response = requests.post(
        f"{IBM_URL}/ml/v1/text/generation?version=2023-05-29",
        headers=headers,
        json=payload
    )

    result = response.json()
    return result["results"][0]["generated_text"]
