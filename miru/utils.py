import json
import logging


def pprint(D: dict):
    output = json.dumps(D, ensure_ascii=False, indent=4)
    logging.info(output)
