import time
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def request_with_retries(endpoint, headers=None, params=None, max_retries=3, backoff_factor=0.3):
    """Makes a GET request with retries and exponential backoff."""
    session = requests.Session()

    retries = Retry(total=max_retries,
                    backoff_factor=backoff_factor,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(endpoint, headers=headers, params=params)
    return response

def handle_rate_limit(response, rate_limit_header="X-RateLimit-Remaining", wait_time=60):
    """Sleeps for a specified time if rate limit is reached."""
    remaining = int(response.headers.get(rate_limit_header, 1))

    if remaining == 0:
        time.sleep(wait_time)
