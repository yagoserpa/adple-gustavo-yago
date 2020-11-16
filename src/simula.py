import collections
import numpy as np
import random
from datetime import datetime

def simula_eventos_discretos(Q,maxt,trans_time,trials):
    random.seed(datetime.now())
    np.seterr(divide='ignore', invalid='ignore')
    dict_time = collections.Counter({})
    probGood = []
    probFake = []
    dim = Q.shape[0]
    for i in range(trials):
        dict_time += simula(Q, maxt, trans_time)
        total_time = 0
        total_time = np.sum(list(dict_time.values()))
        probGood.append(dict_time.get(0, 0) / total_time)
        probFake.append(dict_time.get(55, 0) / total_time)
    state = sum_states(Q,dict_time)
    return state,probGood,probFake

def simula(Q,maxt,trans_time):
    dict_time = {}
    state = 35
    clock = 0

    while clock < maxt:
        row = Q[state]
        pstates = np.where(row > 0)[0]
        if len(pstates) < 1:
            time = maxt - clock
            clock += time
        else:
            rates = row[pstates]
            tlist = np.random.exponential(1/rates)
            time = np.min(tlist)
            clock += time
        if clock > trans_time:
            try:
                dict_time[state] = dict_time.get(state,0) + time
            except KeyError:
                dict_time[state] = time
        if len(pstates) < 1:
            state = state
        else:
            state = pstates[np.argmin(tlist)]
    return collections.Counter(dict_time)

def sum_states(Q,dict_time):
    dim = Q.shape[0]
    total_time = 0
    total_time = np.sum(list(dict_time.values()))
    return np.array([dict_time.get(state, 0) for state in range(dim)]) / total_time
    

