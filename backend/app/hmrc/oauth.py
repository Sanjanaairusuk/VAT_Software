import requests
from app.database.db import SessionLocal
from app.hmrc.helpers import save_hmrc_token, HMRC_TOKEN_URL, HMRC_API_BASE
from datetime import datetime, timedelta

# Exchange code for token
def get_hmrc_token(client_id, client_secret, code, redirect_uri):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(HMRC_TOKEN_URL, data=data)
    response.raise_for_status()
    token_data = response.json()

    db = SessionLocal()
    save_hmrc_token(
        db,
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in")
    )
    db.close()
    return token_data

# Refresh token
def refresh_hmrc_token(client_id, client_secret):
    db = SessionLocal()
    token_entry = db.query(HMRCAuthToken).first()
    if not token_entry or not token_entry.refresh_token:
        db.close()
        raise Exception("No refresh token found.")

    data = {
        "grant_type": "refresh_token",
        "refresh_token": token_entry.refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(HMRC_TOKEN_URL, data=data)
    response.raise_for_status()
    new_token_data = response.json()
    save_hmrc_token(
        db,
        access_token=new_token_data["access_token"],
        refresh_token=new_token_data.get("refresh_token", token_entry.refresh_token),
        expires_in=new_token_data.get("expires_in")
    )
    db.close()
    return new_token_data

# Get valid access token
def get_valid_access_token(client_id, client_secret):
    db = SessionLocal()
    token_entry = db.query(HMRCAuthToken).first()
    db.close()
    if not token_entry:
        raise Exception("No token found. Authorize first.")
    if token_entry.created_at + timedelta(seconds=token_entry.expires_in) < datetime.utcnow():
        token_entry = refresh_hmrc_token(client_id, client_secret)
    return token_entry["access_token"] if isinstance(token_entry, dict) else token_entry.access_token

# Fetch VAT obligations
def get_vat_obligations(client_id, client_secret, vrn):
    access_token = get_valid_access_token(client_id, client_secret)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    url = f"{HMRC_API_BASE}/organisations/vat/{vrn}/obligations?status=O"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
