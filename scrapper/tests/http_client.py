import json
import urllib.request
from dataclasses import dataclass

from pip._vendor import requests


@dataclass
class HttpClient:
    base: str

    def post(self, uri, payload):
        endpoint = self.base + uri
        print(f"HTTP POST: {endpoint}")
        r: requests.Response = requests.post(endpoint, data=json.dumps(payload.__dict__))
        if r.status_code >= 300:
            raise ConnectionError(r)
        return r.content.decode()

    def get(self, uri):
        endpoint = self.base + uri
        print(f"HTTP GET: {endpoint}")
        r: requests.Response = requests.get(endpoint)
        if r.status_code >= 300:
            raise ConnectionError(r)

        return r.content.decode()
