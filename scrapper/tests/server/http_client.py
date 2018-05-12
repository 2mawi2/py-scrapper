import urllib.request
from dataclasses import dataclass


@dataclass
class HttpClient:
    base: str

    def get(self, uri):
        with urllib.request.urlopen(self.base + uri) as res:
            return res.read().decode()
