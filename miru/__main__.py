import json
import os
import logging

from optparse import OptionParser

from miru.parser import Parser
from miru.notion.pages import Pages
from miru.notion.databases import Databases


def pprint(D: dict):
    output = json.dumps(D, ensure_ascii=False, indent=4)
    logging.debug(output)


def update_tags():
    pages = Pages()
    databases = Databases()

    database_id = os.environ.get("NOTION_DATABASE_ID")
    data = {
        "filter": {
            "property": "Tags",
            "multi_select": {
                "does_not_contain": "miru-parsed"
            }
        },
        "page_size": 100
    }
    content = databases.query_database(database_id, data)

    for res in content["results"]:
        page_id = res["id"]
        page = pages.retrieve_page(page_id)

        is_parsed = False
        for ms in page["properties"]["Tags"]["multi_select"]:
            if ms["name"] == "miru-parsed":
                is_parsed = True
                break
        if is_parsed:
            logging.info("Parsed: {}".format(page_id))
        else:
            text = page["properties"]["Names"]["title"][0]["plain_text"]
            _, tags = Parser.novelai_diffusion(text)
            data = {
                "properties": {
                    "Tags": {"multi_select": tags}
                }
            }
            logging.info("Update: {}".format(page_id))
            pages.update_page(page_id, data)


def main():
    update_tags()


if __name__ == "__main__":
    # parse options
    parser = OptionParser()
    parser.add_option(
        "-v", "--verbose",
        action="store_true", dest="verbose", default=False,
        help="debug log")
    (options, _) = parser.parse_args()

    # set log-level
    FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    if options.verbose:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    else:
        logging.basicConfig(level=logging.INFO, format=FORMAT)

    main()
