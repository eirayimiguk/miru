from email import header
import json

from urllib.parse import urljoin

import requests

from miru.notion.client import NotionClient


class Databases(NotionClient):
    def retrieve_database(self, database_id: str):
        url = urljoin(self.base_url, f"databases/{database_id}")
        req = requests.get(url, headers=self.headers, params=None)
        return json.loads(req.text)

    def query_database(self, database_id: str):
        url = urljoin(self.base_url, f"databases/{database_id}/query")
        req = requests.post(url, headers=self.headers, data=None)
        return json.loads(req.text)
