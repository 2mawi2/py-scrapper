import urllib.request
from dataclasses import dataclass


@dataclass
class HttpClient:
    base: str

    def get(self, uri):
        endpoint = self.base + uri
        print(f"HTTP GET: {endpoint}")
        with urllib.request.urlopen(endpoint) as res:
            if res.getcode() >= 300:
                raise ConnectionError()

            return res.read().decode()
