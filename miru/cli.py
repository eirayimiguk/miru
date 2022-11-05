import logging
import random

from optparse import OptionParser

import requests
import climage

from exif import Image
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from miru.batch import get_tags, search_images, update_tags
from miru.utils import chanting_magic_at_random


def status_line():
    return "To exit Ctrl+C"


def update(opts: list = None):
    update_tags()


def search(opts: list = None):
    urls = []
    if len(opts) > 1:
        urls, _ = search_images(opts, page_size=1)
    else:
        urls, _ = search_images(page_size=1)

    for url in urls:
        output_image_to_terminal(url)


def random_chant(opts: list = None):
    if len(opts) > 1:
        length = int(cmd[1])
    else:
        length = 30
    chanting_magic_at_random(length)


def output_image_to_terminal(url: str):
    r = requests.get(url)
    with open("cache/image.png", "wb") as f:
        f.write(r.content)
    img = climage.convert(
        "cache/image.png",
        is_unicode=True,
        is_256color=True,
        is_truecolor=False,
        width=100)
    print(img)


def main():
    try:
        while True:
            cmdline = prompt(">>> ",
                bottom_toolbar=status_line,
                history=FileHistory("cache/history"),
                auto_suggest=AutoSuggestFromHistory()).split(" ")

            cmd = cmdline[0]
            opts = cmdline[1:]

            if cmd == "update":
                update(opts)
            elif cmd == "search":
                search(opts)
            elif cmd == "random":
                random_chant(opts)
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
