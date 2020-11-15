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
    #permut_array = np.empty((0,nusers))
    unique = sorted(unique)
    #for p in unique:
    #    permut_array = np.append(permut_array,np.atleast_2d(p),axis=0)
    return unique
