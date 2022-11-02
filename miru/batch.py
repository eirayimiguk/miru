import os
import logging

from miru.parser import Parser
from miru.notion.blocks import Blocks
from miru.notion.databases import Databases
from miru.notion.pages import Pages

from miru.utils import pprint


# Global Parameters
PARSED_TAG = {"name":"MiruParsed"}
NOTION_DB_TAGS = os.environ.get("NOTION_DB_TAGS")
NOTION_DB_PICTURES = os.environ.get("NOTION_DB_PICTURES")


def update_tags():
    pages = Pages()
    databases = Databases()

    data = {
        "filter": {
            "property": "Tags",
            "multi_select": {
                "does_not_contain": PARSED_TAG["name"]
            }
        },
        "page_size": 100
    }
    content = databases.query_database(NOTION_DB_PICTURES, data)

    for res in content["results"]:
        page_id = res["id"]
        page = pages.retrieve_page(page_id)
        text = page["properties"]["Names"]["title"][0]["plain_text"]
        _, tags = Parser.novelai_diffusion(text, PARSED_TAG)
        data = {"properties":{"Tags":{"multi_select": tags}}}

        logging.info("Update: {}".format(page_id))
        pages.update_page(page_id, data)


def search_images(tags: list) -> list:
    blocks = Blocks()
    databases = Databases()

    conditions = []
    for tag in tags:
        conditions.append({
            "property": "Tags",
            "multi_select": {
                "contains": tag
            }
        })


    data = {"filter": {"and": conditions}}

    urls = []
    res = databases.query_database(NOTION_DB_PICTURES, data)
    for res in res["results"]:
        page_id = res["id"]
        res = blocks.retrieve_block_children(page_id)
        for res in res["results"]:
            urls.append(res["image"]["file"]["url"])
    return urls


def get_words() -> list:
    """
    Tagsデータベースからタグの一覧を取得し、リスト形式で返します

    return
        [{name, mean, tag}, ...,]
    """
    databases = Databases()
    res = databases.query_database(NOTION_DB_TAGS)

    # FIXME: 100件超えるのでページングの実装必須

    words = []
    for r in res["results"]:
        name = r["properties"]["Name"]["title"][0]["text"]["content"]
        mean = r["properties"]["Mean"]["rich_text"][0]["text"]["content"]
        tag = r["properties"]["Tag"]["select"]["name"]

        words.append(
            {
                "name": name,
                "mean": mean,
                "tag" : tag
            }
        )
    return words
