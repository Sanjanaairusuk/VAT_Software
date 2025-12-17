import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone


# ======================================================
# LOAD ENVIRONMENT VARIABLES
# ======================================================

load_dotenv(dotenv_path=Path(__file__).parent / ".env")

BASE_URL = os.getenv("HMRC_BASE_URL")
CLIENT_ID = os.getenv("HMRC_CLIENT_ID")
CLIENT_SECRET = os.getenv("HMRC_CLIENT_SECRET")

print("BASE_URL:", BASE_URL)
print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET loaded:", bool(CLIENT_SECRET))

if not BASE_URL or not CLIENT_ID or not CLIENT_SECRET:
    raise Exception("HMRC credentials not loaded")


# ======================================================
# STEP 1: GET ACCESS TOKEN
# ======================================================

token_url = f"{BASE_URL}/oauth/token"

token_response = requests.post(
    token_url,
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    },
)

print("Token status:", token_response.status_code)
print("Token response:", token_response.json())

token_response.raise_for_status()

access_token = token_response.json()["access_token"]


# ======================================================
# STEP 2: FRAUD HEADERS (RAW STRINGS – NO ENCODING)
# ======================================================

timestamp = (
    datetime.now(timezone.utc)
    .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
)

headers = {
    "Authorization": f"Bearer {access_token}",

    # Client
    "Gov-Client-Connection-Method": "WEB_APP_VIA_SERVER",
    "Gov-Client-Device-ID": "550e8400-e29b-41d4-a716-446655440000",
    "Gov-Client-User-IDs": "session-id=abc123",
    "Gov-Client-Timezone": "UTC+05:30",
    "Gov-Client-Local-IPs": "192.168.1.1",
    "Gov-Client-Public-IP": "203.0.113.1",
    "Gov-Client-Public-IP-Timestamp": timestamp,
    "Gov-Client-Public-Port": "49152",

    "Gov-Client-Screens": "width=1920&height=1080&colour-depth=24&scaling-factor=1",
    "Gov-Client-Window-Size": "width=1920&height=1080",

    "Gov-Client-Browser-JS-User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",

    # Vendor
    "Gov-Vendor-Product-Name": "vat_software",
    "Gov-Vendor-Version": "client=0.1.0",
    "Gov-Vendor-License-IDs": "license-id=vat_software_license",
    "Gov-Vendor-Public-IP": "203.0.113.10",
    "Gov-Vendor-Forwarded": "for=203.0.113.1&by=203.0.113.10",
}


# ======================================================
# STEP 3: VALIDATE FRAUD HEADERS
# ======================================================

fraud_url = f"{BASE_URL}/test/fraud-prevention-headers/validate"

response = requests.get(
    fraud_url,
    headers=headers
)

print("Fraud API status:", response.status_code)
print("Fraud API response:", response.json())
