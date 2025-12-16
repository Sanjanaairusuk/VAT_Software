import requests

# -------------------------
# CONFIGURATION
# -------------------------

VAT_NUMBER = "981598758"  # your sandbox VAT number
ACCESS_TOKEN = "860f1739e17ee0877f1c73d1cbc20fb7"
HMRC_BASE_URL = "https://test-api.service.hmrc.gov.uk"

# -------------------------
# HELPER FUNCTIONS
# -------------------------

def fetch_obligations(vat_number, access_token, from_date="2025-01-01", to_date="2025-12-31"):
    """Fetch VAT obligations for the given VAT number."""
    url = f"{HMRC_BASE_URL}/organisations/vat/{vat_number}/obligations?from={from_date}&to={to_date}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.hmrc.1.0+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("obligations", [])
    else:
        print(f"Failed to fetch obligations: {response.status_code} {response.text}")
        return []

def fetch_return(vat_number, period_key, access_token):
    """Fetch a VAT return for a specific periodKey."""
    url = f"{HMRC_BASE_URL}/organisations/vat/{vat_number}/returns/{period_key}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.hmrc.1.0+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200 and response.text:
        return True  # Return exists
    return False  # No return or 404

# -------------------------
# MAIN SCRIPT
# -------------------------

def main():
    print(f"Fetching VAT obligations for {VAT_NUMBER}...\n")

    obligations = fetch_obligations(VAT_NUMBER, ACCESS_TOKEN)

    print(f"{'Period':<8} {'Status':<8} {'Due Date':<12} {'Return Available':<15}")
    print("-" * 50)

    for obligation in obligations:
        period = obligation["periodKey"]
        status = obligation["status"]
        due = obligation["due"]
        return_available = fetch_return(VAT_NUMBER, period, ACCESS_TOKEN) if status == "F" else False
        print(f"{period:<8} {status:<8} {due:<12} {str(return_available):<15}")

if __name__ == "__main__":
    main()
