import os

class NotionClient:
    def __init__(self):
        self.base_url = "https://api.notion.com/v1/"
        self.notion_key = os.environ.get("NOTION_KEY")
        self.headers = {
            "Authorization": f"Bearer {self.notion_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
