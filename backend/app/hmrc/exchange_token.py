import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

CLIENT_ID = os.getenv("HMRC_CLIENT_ID")
CLIENT_SECRET = os.getenv("HMRC_CLIENT_SECRET")
REDIRECT_URI = os.getenv("HMRC_REDIRECT_URI")
CODE="da9c63054eb443539dfa8bd3524f0cd2"
  # your OAuth code
BASE_URL = os.getenv("HMRC_BASE_URL")

url = f"{BASE_URL}/oauth/token"
payload = {
    "grant_type": "authorization_code",
    "code": CODE,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

response = requests.post(url, data=payload)
tokens = response.json()
print(tokens)
