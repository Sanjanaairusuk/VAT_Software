import requests

CLIENT_ID = "juUaMRwkOygCYfP6zQgHVCxBVG9b"
CLIENT_SECRET = "95d59476-5e79-492b-9f9e-6a054f0964b2"

REFRESH_TOKEN = "bdc209fb94e192d1ea7113682d22b0a2"

url = "https://test-api.service.hmrc.gov.uk/oauth/token"

data = {
    "grant_type": "refresh_token",
    "refresh_token": REFRESH_TOKEN,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

response = requests.post(url, data=data)

print("Status:", response.status_code)
print(response.json())
