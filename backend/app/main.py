import os
import requests
from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from .database.db import SessionLocal, Base, engine
from .models import VATObligation
from .hmrc import fetch_obligations
from datetime import datetime

app = FastAPI()

HMRC_CLIENT_ID = os.getenv("HMRC_CLIENT_ID")
HMRC_CLIENT_SECRET = os.getenv("HMRC_CLIENT_SECRET")
HMRC_REDIRECT_URI = os.getenv("HMRC_REDIRECT_URI")
HMRC_BASE_URL = os.getenv("HMRC_BASE_URL")

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home page
@app.get("/")
def home():
    return {"message": "VAT FastAPI app is running!"}

# Get obligations (mock)
@app.get("/obligations/{vrn}")
def get_obligations(vrn: str, db: Session = Depends(get_db)):
    db.query(VATObligation).filter(VATObligation.vrn == vrn).delete()
    data = fetch_obligations(vrn)
    for o in data:
        period_start = datetime.strptime(o["period_start"], "%Y-%m-%d").date()
        period_end = datetime.strptime(o["period_end"], "%Y-%m-%d").date()
        due = datetime.strptime(o["due"], "%Y-%m-%d").date()
        db.add(VATObligation(
            vrn=vrn,
            period_start=period_start,
            period_end=period_end,
            due=due,
            status=o["status"]
        ))
    db.commit()
    return data

# HMRC OAuth callback (optional)
@app.get("/auth/callback")
def auth_callback(request: Request, vrn: str, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    token_url = f"{HMRC_BASE_URL}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": HMRC_REDIRECT_URI,
        "client_id": HMRC_CLIENT_ID,
        "client_secret": HMRC_CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_resp = requests.post(token_url, data=payload, headers=headers)
    if token_resp.status_code != 200:
        raise HTTPException(status_code=token_resp.status_code, detail=token_resp.text)

    access_token = token_resp.json()["access_token"]
    obligations_url = f"{HMRC_BASE_URL}/organisations/vat/{vrn}/obligations"
    params = {"from": "2023-01-01", "to": "2025-12-31"}
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.hmrc.1.0+json"
    }
    obligations_resp = requests.get(obligations_url, headers=headers, params=params)
    if obligations_resp.status_code != 200:
        raise HTTPException(status_code=obligations_resp.status_code, detail=obligations_resp.text)

    obligations_data = obligations_resp.json().get("obligations", [])
    for o in obligations_data:
        period_start = datetime.strptime(o.get("start"), "%Y-%m-%d").date()
        period_end = datetime.strptime(o.get("end"), "%Y-%m-%d").date()
        due = datetime.strptime(o.get("due"), "%Y-%m-%d").date()
        received_date = datetime.strptime(o.get("received"), "%Y-%m-%d").date() if o.get("received") else None
        db_obj = VATObligation(
            vrn=vrn,
            period_start=period_start,
            period_end=period_end,
            due=due,
            status=o.get("status"),
            received_date=received_date
        )
        db.add(db_obj)
    db.commit()
    return {"message": "HMRC authorization successful", "stored_obligations": len(obligations_data)}

# Create tables
Base.metadata.create_all(bind=engine)
