import os
import logging

from typing import Tuple

from miru.parser import Parser
from miru.notion.blocks import Blocks
from miru.notion.databases import Databases
from miru.notion.pages import Pages


# Global Parameters
PARSED_TAG = {"name":"MiruParsed"}
NOTION_DB_TAGS = os.environ.get("NOTION_DB_TAGS")
NOTION_DB_IMAGES = os.environ.get("NOTION_DB_IMAGES")


def search_images(tags: list=None, start_cursor=None, enable_or_search: bool = False) -> Tuple[list, str]:
    """
    NAI Diffusionデータベースからすべての画像のURLを取得し、リスト形式で返します

    return
        ["url", ...,]
    """
    blocks = Blocks()
    databases = Databases()

    properties = []
    if not tags is None:
        for tag in tags:
            properties.append({"property": "Tags", "multi_select": {"contains": tag}})

    if enable_or_search:
        data = {"filter": {"or": properties}}
    else:
        data = {"filter": {"and": properties}}

    if not start_cursor is None:
        data["start_cursor"] = start_cursor

    data["page_size"] = 5

    urls = []
    response = databases.query_database(NOTION_DB_IMAGES, data)
    for res in response["results"]:
        page_id = res["id"]
        res = blocks.retrieve_block_children(page_id)
        for res in res["results"]:
            urls.append(res["image"]["file"]["url"])

    if response["has_more"]:
        return urls, response["next_cursor"]
    else:
        return urls, ""


def get_tags() -> list:
    """
    Tagsデータベースからすべてのタグを取得し、リスト形式で返します

    return
        [{name, mean, tag}, ...,]
    """
    databases = Databases()

    tags, data, has_more = [], {}, True
    while has_more:
        response = databases.query_database(NOTION_DB_TAGS, data=data)
        for r in response["results"]:
            tags.append({
                "name": r["properties"]["Name"]["title"][0]["text"]["content"],
                "mean": r["properties"]["Mean"]["rich_text"][0]["text"]["content"],
                "tag" : r["properties"]["Tag"]["select"]["name"]
            })
        has_more = response["has_more"]
        data["start_cursor"] = response["next_cursor"]
    return tags


def update_tags():
    """
    NAI Diffusionデータベース内でTag付けが完了していないページに対してタグ付けを行います

    return
        None
    """
    pages = Pages()
    databases = Databases()

    data = {
        "filter": {
            "property": "Tags",
            "multi_select": {
                "does_not_contain": PARSED_TAG["name"]
            }
        }
    }

    has_more = True
    while has_more:
        response = databases.query_database(NOTION_DB_IMAGES, data)
        for res in response["results"]:
            page_id = res["id"]
            page = pages.retrieve_page(page_id)
            page_title = page["properties"]["Names"]["title"][0]["plain_text"]
            _, tags = Parser.novelai_diffusion(page_title, PARSED_TAG)

            logging.info("Update: {}".format(page_id))
            update_page_data = {"properties":{"Tags":{"multi_select": tags}}}
            status = pages.update_page(page_id, update_page_data)
            logging.info("{}".format(status))
        has_more = response["has_more"]
        data["start_cursor"] = response["next_cursor"]
