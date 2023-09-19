import requests

class BaseConnector:
    def __init__(self, endpoint, headers):
        self.endpoint = endpoint
        self.headers = headers

    def fetch_data(self, params):
        """A generic function to fetch data from an API."""
        response = requests.get(self.endpoint, headers=self.headers, params=params)
        return response.json()
