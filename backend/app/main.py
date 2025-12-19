from fastapi import FastAPI, HTTPException
import os
import requests
from dotenv import load_dotenv
from datetime import date

load_dotenv()

app = FastAPI()

HMRC_CLIENT_ID = os.getenv("HMRC_CLIENT_ID")
HMRC_CLIENT_SECRET = os.getenv("HMRC_CLIENT_SECRET")
HMRC_REDIRECT_URI = os.getenv("HMRC_REDIRECT_URI")
HMRC_BASE_URL = os.getenv("HMRC_BASE_URL")

ACCESS_TOKEN = None


@app.get("/")
def root():
    return {"message": "VAT Software Running"}


@app.get("/hmrc/login")
def hmrc_login():
    auth_url = (
        f"{HMRC_BASE_URL}/oauth/authorize"
        f"?response_type=code"
        f"&client_id={HMRC_CLIENT_ID}"
        f"&scope=read:vat write:vat"
        f"&redirect_uri={HMRC_REDIRECT_URI}"
    )
    return {"auth_url": auth_url}


@app.get("/auth/callback")
def auth_callback(code: str):
    global ACCESS_TOKEN

    token_url = f"{HMRC_BASE_URL}/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": HMRC_REDIRECT_URI,
        "client_id": HMRC_CLIENT_ID,
        "client_secret": HMRC_CLIENT_SECRET,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=response.text)

    ACCESS_TOKEN = response.json()["access_token"]
    return {"message": "HMRC authorization successful"}

@app.get("/vat/obligations")
def get_vat_obligations(
    vrn: str,
    from_date: str = "2023-01-01",
    to_date: str = "2025-12-31"
):
    if not ACCESS_TOKEN:
        raise HTTPException(status_code=401, detail="Not authorized with HMRC")

    url = f"{HMRC_BASE_URL}/organisations/vat/{vrn}/obligations"

    params = {
        "from": from_date,
        "to": to_date
    }

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/vnd.hmrc.1.0+json"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
