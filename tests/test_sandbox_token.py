from app.hmrc.exchange_token import get_access_token


# Replace with your sandbox client credentials
CLIENT_ID = "your_sandbox_client_id"
CLIENT_SECRET = "your_sandbox_client_secret"

token_data = get_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
access_token = token_data.get("access_token")

print("Access token:", access_token)
