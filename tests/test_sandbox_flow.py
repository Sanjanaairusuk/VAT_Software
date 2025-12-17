import os
import json
from datetime import datetime, timezone
import requests

# --- CONFIG ---
ACCESS_TOKEN = "ec0c23cbba687fc6fe0db3bd50464ce7"  # Your sandbox access token
VRN = "981598758"
URL = f"https://test-api.service.hmrc.gov.uk/organisations/vat/{VRN}/obligations?from=2024-01-01&to=2024-12-31"

# --- AUDIT LOGGER ---
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "audit.log")

def log_event(user_id, action, details=None):
    details_str = f" | details: {details}" if details else ""
    timestamp = datetime.now(timezone.utc).isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - user_id={user_id} | action={action}{details_str}\n")

# --- API CALL ---
def test_sandbox_api():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/vnd.hmrc.1.0+json"
    }

    response = requests.get(URL, headers=headers)

    print("Status code:", response.status_code)
    print("Response body:", json.dumps(response.json(), indent=2))

    log_event("codespace_user", "sandbox_api_test", {
        "url": URL,
        "status": response.status_code
    })

# --- RUN TEST ---
if __name__ == "__main__":
    test_sandbox_api()
