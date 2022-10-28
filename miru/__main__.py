import json

from miru.notion.client import NotionClient
from miru.notion.databases import Databases
from .notion.pages import Pages

pages = Pages()
databases = Databases()

database_id = None

content = databases.retrieve_database(database_id)
print(json.dumps(content, ensure_ascii=False, indent=4))
content = databases.query_database(database_id)
print(json.dumps(content, ensure_ascii=False, indent=4))
