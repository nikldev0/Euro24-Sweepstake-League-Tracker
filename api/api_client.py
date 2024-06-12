import requests 
from config.config import API_KEY, API_HOST

class ApiClient:
    def __init__(self):
        self.base_url = f"https://{API_HOST}"
        self.headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': API_HOST
        }

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
