import numpy as np
import itertools
from collections import Counter

def perms(Array,nusers):
    permut = set(list(itertools.permutations(Array,nusers)))
    seen = set()
    unique = []
    for x in permut:
        srtd = tuple(sorted(x))
        if srtd not in seen:
            unique.append(x)
            seen.add(srtd)
    unique = sorted(unique)
    return unique
