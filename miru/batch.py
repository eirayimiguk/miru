import os
import logging
import json

from typing import Tuple

from miru.parser import NAIDiffusion
from miru.notion.blocks import Blocks
from miru.notion.databases import Databases
from miru.notion.pages import Pages
from miru.utils import get_text_chunks


# Global Parameters
NOTION_DB_TAGS = os.environ.get("NOTION_DB_TAGS")
NOTION_DB_IMAGES = os.environ.get("NOTION_DB_IMAGES")


def search_images(tags: list = None, page_size: int = 1, start_cursor=None, enable_or_search: bool = False) -> Tuple[list, str]:
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

    data["page_size"] = page_size

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
    blocks = Blocks()
    databases = Databases()
    parser = NAIDiffusion()

    data = {
        "filter": {
            "property": "Tags",
            "multi_select": {
                "does_not_contain": parser.parsed_tag
            }
        }
    }

    has_more = True
    while has_more:
        response = databases.query_database(NOTION_DB_IMAGES, data)
        for page in response["results"]:
            child = blocks.retrieve_block_children(page["id"])
            chunks = get_text_chunks(child["results"][0]["image"]["file"]["url"])

            tags = parser.parse(chunks["Description"])
            comment = json.loads(chunks["Comment"])
            update_page_data = {
                "properties": {
                    "Tags": {"multi_select": tags},
                    "Software": {"rich_text": [{"text": {"content": chunks["Software"]}}]},
                    "Source": {"rich_text": [{"text": {"content": chunks["Source"]}}]},
                    "Steps": {"number": comment["steps"]},
                    "Sampler": {"rich_text": [{"text": {"content": comment["sampler"]}}]},
                    "Seed": {"number": comment["seed"]},
                    "Strength": {"number": comment["strength"]},
                    "Noise": {"number": comment["noise"]},
                    "Scale": {"number": comment["scale"]},
                    "Prompt": {"rich_text": [{"text": {"content": chunks["Description"]}}]},
                    "Negative": {"rich_text": [{"text": {"content": comment["uc"]}}]},
                }
            }
            status = pages.update_page(page["id"], update_page_data)
            logging.debug(status)
        has_more = response["has_more"]
        data["start_cursor"] = response["next_cursor"]
