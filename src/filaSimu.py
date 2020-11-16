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
        addEventos(origem, escolheDestino(origem), tline[origem][0])
        addEventos(origem, escolheDestino(origem), tline[origem][1])

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

    

 
dict_time2 = collections.Counter({})
nusers = 5
lambda0=0.1
lambda1=0.2
rate1 = 2
rate2 = 2
globalId = 0
tempo_trans = 0
max_time= 6

#todos estados possiveis
array = list(states_map.values()) * nusers
states = bib.perms(array,nusers)
    
states_number = []
#verifica estados possiveis
for i in range(len(states)):
    states_number.append([states[i].count("color1"),states[i].count("color2"),states[i].count("color3"),states[i].count("color4")])
 
#estados ordenados
states_number= sorted(states_number,reverse=1)
     
#dicionario com os estados
dict = {mergeString(tuple(key)): idx for idx, key in enumerate(states_number)}
nstates = len(states_number)
probGood = []
probFake = []   

probGood2= []
probFake2= []
varGood = []
varFake = []
for i in range(100):
    random.seed(datetime.now())
    state = 35
    clock = 0
    dict_time = {}
    tline = {}
    filaEventos = []
   
    #inicializa timeline
    initTline(nusers)
    while(clock < max_time):
        filaEventos = []
        samples = []
        enviaMensagens(nusers)
        samples = [evento.tempo for evento in filaEventos]
        #print(samples)
        time = np.min(samples)
        if(state == 55 or state == 0):
            time = max_time - clock
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
    if(i > 5):
        total_time = 0
        total_time = np.sum(list(dict_time.values()))
        probGood2.append(dict_time.get(0, 0) / total_time)
        probFake2.append(dict_time.get(55, 0)/ total_time)
        dict_time2 = collections.Counter({})
    if( ((i % 5) == 0) and (i > 5)):
        probGood.append(np.mean(probGood2))
        probFake.append(np.mean(probFake2))
        varGood.append(np.var(probGood2))
        varFake.append(np.var(probFake2))
        probGood2 = []
        probFake2 = []

print("Média Probabilidade do Estado All Non Fake {}".format(np.mean(probGood)))
print("Variancia Probabilidade do Estado All Non Fake {}".format(np.mean(varGood)))
confinteru=np.mean(probGood)+1.96*(np.std(probGood)/np.sqrt(len(probGood)))
confinterl=np.mean(probGood)-1.96*(np.std(probGood)/np.sqrt(len(probGood)))
print("IC superior Probabilidade do Estado All Non Fake {}".format(confinteru))
print("IC inferior Probabilidade do Estado All Non Fake {}".format(confinterl))
print("\n")
print("Média Probabilidade do Estado All Fake {}".format(np.mean(probFake)))
print("Variancia Probabilidade do Estado All Fake {}".format(np.mean(varFake)))
confinteru=np.mean(probFake)+1.96*(np.std(probFake)/np.sqrt(len(probFake)))
confinterl=np.mean(probFake)-1.96*(np.std(probFake)/np.sqrt(len(probFake)))
print("IC superior Probabilidade do Estado All Fake {}".format(confinteru))
print("IC inferior Probabilidade do Estado All Fake {}".format(confinterl))

#np.seterr(divide='ignore', invalid='ignore')
#total_time = 0
#total_time = np.sum(list(dict_time2.values()))
#print(total_time)
#print(np.array([dict_time2.get(state, 0) for state in range(nstates)]) / total_time) 

    

