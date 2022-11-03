import logging
import random

from optparse import OptionParser

from miru.batch import get_tags, search_images, update_tags


def chanting_magic_at_random(length: int = 10):
    tags = get_tags()

    spell = []
    for _ in range(length):
        index = random.randint(0, len(tags) - 1)
        spell.append(tags[index]["name"])
    print(", ".join(spell))


def search():
    urls = search_images(["looking at viewer"])
    print(urls)


def update():
    update_tags()


def main():
    update()


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
