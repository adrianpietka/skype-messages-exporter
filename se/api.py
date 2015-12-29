import json
import requests

class Api:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def save_messages(self, messages):
        payload = json.dumps(messages)
        headers = {"content-type": "application/json"}
        return requests.post(self.api_url, data = payload, headers = headers)