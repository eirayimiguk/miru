import random

from miru.batch import get_tags

def chanting_magic_at_random(length: int = 10):
    tags = get_tags()

    spell = []
    for _ in range(length):
        index = random.randint(0, len(tags) - 1)
        spell.append(tags[index]["name"])
    return ",".join(spell)
