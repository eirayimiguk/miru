import json

from miru.notion.client import NotionClient
from .notion.pages import Pages

pages = Pages()
content = pages.retrieve_page("2e0b7c86c23e47e5aa5703a81a413987")
print(json.dumps(json.loads(content), indent=4))

