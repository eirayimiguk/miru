import random

from urllib.request import urlopen

import png
import climage

# from miru.batch import get_tags
#
#
# def chanting_magic_at_random(length: int = 10):
#     tags = get_tags()
#
#     spell = []
#     for _ in range(length):
#         index = random.randint(0, len(tags) - 1)
#         spell.append(tags[index]["name"])
#     return ",".join(spell)


def get_text_chunks(image_url: str = None, image_file: str = None):
    chunks = {}

    if not image_file is None:
        r = png.Reader(filename=image_file)
    elif not image_url is None:
        r = png.Reader(file=urlopen(image_url))
    else:
        return {}

    for chunk in r.chunks():
        if chunk[0] == b"tEXt":
            key, value = chunk[1].decode("utf-8").replace("\x00", "|").split("|")
            chunks[key] = value
    return chunks


def output_image_to_terminal(url: str):
    img = climage.convert(
        urlopen(url),
        is_unicode=True,
        is_256color=False,
        is_truecolor=True,
        width=80)
    print(img)
