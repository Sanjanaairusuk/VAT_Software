import requests

vat_number = "981598758"  # your VAT number
access_token = "860f1739e17ee0877f1c73d1cbc20fb7"

url = f"https://test-api.service.hmrc.gov.uk/organisations/vat/{vat_number}/obligations?from=2025-01-01&to=2025-12-31"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.hmrc.1.0+json"
}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print("Response JSON:", response.json())
