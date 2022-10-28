from urllib.parse import urljoin

import requests

from miru.notion.client import NotionClient


class Pages(NotionClient):
    def retrieve_page(self, page_id: str):
        url = urljoin(self.base_url, f"pages/{page_id}")
        req = requests.get(url, headers=self.headers, params=None)
        return req.content
