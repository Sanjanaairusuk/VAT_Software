import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import time

LAST_REQUEST_TIME = 0
RPS = 3
MIN_INTERVAL = 1 / RPS  # seconds per request

def rate_limited_request():
    global LAST_REQUEST_TIME
    elapsed = time.time() - LAST_REQUEST_TIME
    if elapsed < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - elapsed)
    LAST_REQUEST_TIME = time.time()

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def hmrc_request(url, method="GET", headers=None, data=None):
    rate_limited_request()  # respect 3 RPS
    response = requests.request(method, url, headers=headers, json=data, timeout=10)
    
    if response.status_code in [429, 500, 502, 503, 504]:
        response.raise_for_status()  # triggers retry
    return response
