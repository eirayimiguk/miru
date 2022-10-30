import json

from urllib.parse import urljoin

import requests

from miru.notion.client import NotionClient


class Databases(NotionClient):
    def retrieve_database(self, database_id: str):
        endpoint = f"databases/{database_id}"
        url = urljoin(self.base_url, endpoint)

        req = requests.get(url, headers=self.headers, params=None)
        return json.loads(req.text)

    def query_database(self, database_id: str, data: dict = {}):
        endpoint = f"databases/{database_id}/query"
        url = urljoin(self.base_url, endpoint)

        req = requests.post(url, headers=self.headers, json=data)
        return json.loads(req.text)
