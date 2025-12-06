import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_azure_ai_credentials():
    endpoint = os.getenv("AZURE_AI_INFERENCE_ENDPOINT")
    key = os.getenv("AZURE_AI_INFERENCE_KEY")
    
    print(f"Endpoint: {endpoint}")
    print(f"Key: {key[:10]}...")
    
    # Test basic connectivity
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Try to get models list
    models_url = f"{endpoint}/models"
    
    try:
        response = requests.get(models_url, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_azure_ai_credentials()