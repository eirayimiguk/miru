import os
import logging

from miru.parser import Parser
from miru.notion.blocks import Blocks
from miru.notion.databases import Databases
from miru.notion.pages import Pages


# Global Parameters
PARSED_TAG = {"name":"MiruParsed"}
NOTION_DB_TAGS = os.environ.get("NOTION_DB_TAGS")
NOTION_DB_IMAGES = os.environ.get("NOTION_DB_IMAGES")


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
        },
        "page_size": 3
    }

    response = databases.query_database(NOTION_DB_IMAGES, data)
    for res in response["results"]:
        page_id = res["id"]
        page = pages.retrieve_page(page_id)
        text = page["properties"]["Names"]["title"][0]["plain_text"]
        _, tags = Parser.novelai_diffusion(text, PARSED_TAG)
        data = {"properties":{"Tags":{"multi_select": tags}}}

        status = pages.update_page(page_id, data)
        logging.info("Update: {}<{}>".format(page_id, status))


def search_images(tags: list, is_or_search: bool = False) -> list:
    """
    NAI Diffusionデータベースからすべての画像のURLを取得し、リスト形式で返します

    return
        ["url", ...,]
    """
    blocks = Blocks()
    databases = Databases()

    properties = []
    for tag in tags:
        properties.append({"property": "Tags", "multi_select": {"contains": tag}})

    if is_or_search:
        data = {"filter": {"or": properties}}
    else:
        data = {"filter": {"and": properties}}

    urls, has_more = [], True
    while has_more:
        response = databases.query_database(NOTION_DB_IMAGES, data)
        for res in response["results"]:
            page_id = res["id"]
            res = blocks.retrieve_block_children(page_id)
            for res in res["results"]:
                urls.append(res["image"]["file"]["url"])
        has_more = response["has_more"]
        data["start_cursor"] = response["next_cursor"]
    return urls


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
