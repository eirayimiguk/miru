import logging
import json

from optparse import OptionParser

from miru.notion.pages import Pages
from miru.batch import search_images, update_tags
from miru.utils import get_text_chunks, output_image_to_terminal


def main():
    update_tags()
    urls, _ = search_images(page_size=1)
    for url in urls:
        output_image_to_terminal(url)



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
