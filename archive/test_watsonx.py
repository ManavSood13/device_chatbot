import requests
import json

IBM_API_KEY = "xypQMF6Msyb0fnKU_g9hsPE_2_0bmjkt48Z4sm_Px-QL"
IBM_URL = "https://us-south.ml.cloud.ibm.com"
MODEL_ID = "ibm/granite-3-8b-instruct"

# Step 1: Get access token
auth_url = "https://iam.cloud.ibm.com/identity/token"
auth_headers = {"Content-Type": "application/x-www-form-urlencoded"}
auth_data = f"apikey={IBM_API_KEY}&grant_type=urn:ibm:params:oauth:grant-type:apikey"

auth_response = requests.post(auth_url, headers=auth_headers, data=auth_data)
print("Auth status:", auth_response.status_code)
print("Auth response:", auth_response.text)

try:
    access_token = auth_response.json()["access_token"]
except Exception as e:
    print("❌ Error fetching token:", e)
    print("Response:", auth_response.text)
    exit()

# Step 2: Send a message to Watsonx
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

payload = {
    "model_id": MODEL_ID,
    "input": "Suggest a laptop under ₹1 lakh for gaming.",
    "project_id": "9958f02b-32a5-4e87-8b5e-3f3b45163c13",  # 👈 add this line
    "parameters": {"max_new_tokens": 150}
}


response = requests.post(
    f"{IBM_URL}/ml/v1/text/generation?version=2023-05-29",
    headers=headers,
    json=payload
)

print("\nResponse Status:", response.status_code)
print("Raw Response:", response.text)

if response.status_code == 200:
    result = response.json()
    print("\nAI Response:\n", result["results"][0]["generated_text"])
else:
    print("❌ Request failed.")
