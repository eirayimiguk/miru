import json

from urllib.parse import urljoin

import requests

from miru.notion.client import NotionClient


class Pages(NotionClient):
    def retrieve_page(self, page_id: str):
        endpoint = f"pages/{page_id}"
        url = urljoin(self.base_url, endpoint)

        req = requests.get(url, headers=self.headers, params=None)
        return json.loads(req.text)

    def update_page(self, page_id: str, data: dict = {}):
        endpoint = f"pages/{page_id}"
        url = urljoin(self.base_url, endpoint)

        req = requests.patch(url, headers=self.headers, json=data)
        return json.loads(req.text)

