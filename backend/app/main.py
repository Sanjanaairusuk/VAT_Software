from fastapi import FastAPI, HTTPException
from app.database.db import Base, engine
from app.hmrc.oauth import get_hmrc_token, get_vat_obligations
from app.hmrc.helpers import build_authorization_url

CLIENT_ID = "juUaMRwkOygCYfP6zQgHVCxBVG9b"
CLIENT_SECRET = "95d59476-5e79-492b-9f9e-6a054f0964b2"
REDIRECT_URI = "http://localhost:8000/auth/callback"
VRN = "981598758"

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {"message": "VAT Software Running"}

# Generate HMRC login URL
@app.get("/hmrc/login")
def hmrc_login():
    auth_url = build_authorization_url(CLIENT_ID, REDIRECT_URI)
    return {"auth_url": auth_url}

# Callback endpoint to exchange code for tokens
@app.get("/auth/callback")
def hmrc_callback(code: str):
    try:
        token_data = get_hmrc_token(CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI)
        return {"message": "Token saved successfully", "token_data": token_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Fetch VAT obligations
@app.get("/vat/obligations")
def vat_obligations():
    try:
        obligations = get_vat_obligations(CLIENT_ID, CLIENT_SECRET, VRN)
        return obligations
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
