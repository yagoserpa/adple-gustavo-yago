# -*- coding: utf-8 -*-

import numpy as np
import itertools
import biblioteca as bib
import scipy.linalg as la
import matplotlib.pyplot as plt
import simula
import random
from datetime import datetime
import collections
random.seed(datetime.now())

class Evento:
   def __init__(self,id,remetente,destinatario,tempo,tipo):
       self.id = id
       self.remetente = remetente
       self.destinatario = destinatario
       self.tempo = tempo
       self.tipo = tipo
       #print("adicionado evento {} do remetente {} para {} no tempo {}, tipo {}".format(id,remetente,destinatario,tempo,tipo))

def escolheOrigem():
    return random.choices(['0','1','2','3','4'])[0]

def escolheDestino(a):
    weights = []
    for i in range(nusers):
        if('{}'.format(i) != a):
          weights.append(0.25)
        else:
          weights.append(0)      
    return int(random.choices(['0','1','2','3','4'],weights)[0])

def mergeString(list):
    word = ''.join(str(x) for x in list)
    return word

def nextArrival(taxa):
    return np.random.exponential(1/taxa)

def initTline(nusers):     
    for i in range(nusers):
        tline['{}'.format(i)] = [0,1]

def addEventos(de,para,tipo):
    global globalId
    globalId = globalId + 1
    taxa = 0
    if(tipo == 1):
        taxa = rate2 + lambda1
    else:
        taxa = rate1 + lambda0
    filaEventos.append(Evento(globalId,de,para,nextArrival(taxa),tipo))

def enviaMensagens(nusers):
    for i in range(nusers):
        origem = '{}'.format(i)
        addEventos(origem, escolheDestino(origem) , tline[origem][0])
        addEventos(origem, escolheDestino(origem) , tline[origem][1])

def modificaTimeline(destino,tipo):
    tline['{}'.format(destino)][0] = tline['{}'.format(destino)][1]
    tline['{}'.format(destino)][1] = tipo

def trataEventos(argumento,filaEventos):
    destinos = [evento.destinatario for evento in filaEventos]
    tipos = [evento.tipo for evento in filaEventos]
    modificaTimeline(destinos[argumento],tipos[argumento])

def validaEstado():
    estados = []
    for i in range(nusers):
        estados.append(states_map[mergeString([tline['{}'.format(i)][0],tline['{}'.format(i)][1]])])
    estado = mergeString([estados.count("color1"),estados.count("color2"),estados.count("color3"),estados.count("color4")])
    return estado  


states_map = {
           '00': "color1", # blue , no fake news
           '01': "color2", # orange , fake new at bottom
           '10': "color3", # yellow , fake new at top
           '11': "color4" # red , two fake news
}

nusers = 5
lambda0=0.1
lambda1=0.2
rate1 = 1
rate2 = 1
globalId = 0
tempo_trans = 0
    
#todos estados possiveis
array = list(states_map.values()) * nusers
states = bib.perms(array,nusers)
    
states_number = []
#verifica estados possiveis
for i in range(len(states)):
   states_number.append([states[i].count("color1"),states[i].count("color2"),states[i].count("color3"),states[i].count("color4")])
    
states_number= sorted(states_number,reverse=1)
    
dict = {mergeString(tuple(key)): idx for idx, key in enumerate(states_number)}
nstates = len(states_number)

dict_time2 = collections.Counter({})

inival = 0.01
inc = 0.01
max_time= 24
initstate = 35

interval = np.linspace(inival,max_time,max_time*1000)
transient = np.zeros((len(interval),nstates))

for index, t in enumerate(interval):
    print(index,t)
    random.seed(datetime.now())
    
    state = 35
    clock = 0
    dict_time = {}
    tline = {}
    filaEventos = []
   
    #inicializa timeline
    initTline(nusers)
    
    while(clock < t):
        filaEventos = []
        samples = []
        enviaMensagens(nusers)
        samples = [evento.tempo for evento in filaEventos]
        #print(samples)
        time = np.min(samples)
        if(state == 55 or state == 0):
            time = t - clock
        clock += time
        if clock > tempo_trans:
            try:
               dict_time[state] = dict_time.get(state,0) + time
            except KeyError:
               dict_time[state] = time
        if(state == 55 or state == 0):
            break
        else:
            trataEventos(np.argmin(samples),filaEventos)
            state = dict[validaEstado()]
        #print(state)
        #print(dict_time)
    dict_time2 += collections.Counter(dict_time)
    total_time = 0
    total_time = np.sum(list(dict_time2.values()))
    #print(total_time)    
    transient[index] = (np.array([dict_time2.get(state, 0) for state in range(nstates)]) / total_time) 
np.seterr(divide='ignore', invalid='ignore')

total_time = 0
total_time = np.sum(list(dict_time2.values()))
print(total_time)    
print(np.array([dict_time2.get(state, 0) for state in range(nstates)]) / total_time) 

x = transient[:,nstates-1][np.logical_not(np.isnan(transient[:,nstates-1]))]
y = transient[:,0][np.logical_not(np.isnan(transient[:,0]))]
ci1 = 1.96 * np.std(x)/np.sqrt(len(x))
ci0 = 1.96 * np.std(y)/np.sqrt(len(y))
plt.plot(interval,transient[:,nstates-1],'b--' , label = "state (0 0 0 5): all fake")
plt.plot(interval,transient[:,0],'r', label = "state (5 0 0 0): all non fake")
#print(transient[:,nstates-1])
plt.legend(loc="best")
plt.xlabel('Time')
plt.ylabel('State Probability')
plt.fill_between(interval, (transient[:,nstates-1]-ci1), (transient[:,nstates-1]+ci1), color='skyblue', alpha=1.0)
plt.fill_between(interval, (transient[:,0]-ci0), (transient[:,0]+ci0), color='tomato', alpha=1.0)
plt.show()
    

