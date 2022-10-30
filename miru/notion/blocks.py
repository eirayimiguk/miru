import json

from urllib.parse import urljoin

import requests

from miru.notion.client import NotionClient


class Blocks(NotionClient):
    def retrieve_block_children(self, block_id: str):
        endpoint = f"blocks/{block_id}/children"
        url = urljoin(self.base_url, endpoint)

        req = requests.get(url, headers=self.headers, params=None)
        return json.loads(req.text)
