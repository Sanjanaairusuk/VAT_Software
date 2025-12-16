from urllib.parse import urlencode

HMRC_AUTH_URL = "https://test-api.service.hmrc.gov.uk/oauth/authorize"
HMRC_TOKEN_URL = "https://test-api.service.hmrc.gov.uk/oauth/token"
HMRC_API_BASE = "https://test-api.service.hmrc.gov.uk"


def build_authorization_url(client_id: str, redirect_uri: str) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": "read:vat write:vat",
        "redirect_uri": redirect_uri,
    }
    return f"{HMRC_AUTH_URL}?{urlencode(params)}"


def save_hmrc_token(*args, **kwargs):
    # TEMP dummy function (ok for now)
    return True
