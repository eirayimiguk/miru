import logging
import random

from optparse import OptionParser

import requests
import climage

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from miru.batch import get_tags, search_images, update_tags
from miru.utils import chanting_magic_at_random


def status_line():
    return "To exit Ctrl+C"


def main():
    try:
        while True:
            cmd = prompt(">>> ",
                bottom_toolbar=status_line,
                history=FileHistory("cache/history"),
                auto_suggest=AutoSuggestFromHistory()).split(" ")

            if cmd[0] == "update":
                update_tags()
            elif cmd[0] == "search":
                urls = []
                if len(cmd) > 1:
                    urls, next_cursor = search_images(cmd[1:], page_size=3)
                else:
                    urls, next_cursor = search_images(page_size=3)
                for url in urls:
                    r = requests.get(url)
                    with open("cache/image.png", "wb") as img:
                        img.write(r.content)
                        o = climage.convert("cache/image.png", is_256color=False, is_truecolor=True, width=128)
                        print(o)
            elif cmd[0] == "random":
                if len(cmd) > 1:
                    length = int(cmd[1])
                else:
                    length = 30
                chanting_magic_at_random(length)
    except KeyboardInterrupt:
        pass


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
