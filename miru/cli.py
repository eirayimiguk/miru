import logging

from optparse import OptionParser

import png

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

from miru.batch import get_tags, search_images, update_tags
from miru.utils import chanting_magic_at_random, get_text_chunks


def status_line():
    return "To exit Ctrl+C"


def update(opts: list = None):
    update_tags()


def search(opts: list = []):
    urls = []
    if len(opts) > 1:
        urls, _ = search_images(opts, page_size=3)
    else:
        urls, _ = search_images(page_size=3)

    return urls


def random_chant(opts: list = None):
    if len(opts) > 1:
        length = int(opts)
    else:
        length = 30
    chanting_magic_at_random(length)




def prompt():
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
            elif cmd == "exif":
                get_exif()
    except KeyboardInterrupt:
        pass


def main():
    prompt()


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
