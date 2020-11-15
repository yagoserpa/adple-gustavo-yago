import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from random import SystemRandom
import llist 
from llist import sllist,sllistnode



class Evento:
   def __init__(self, id, tipo, tempo,remetente,destinatario):
       self.id = id
       self.tipo = tipo
       self.tempo = tempo
       self.remetente = remetente
       self.destinatario = destinatario


def nextArrival(alfa):
    return np.random.exponential(alfa)

def plot(G,nusers):
    for i in range(nusers):
        state = G.nodes[i]["linepos1"] + G.nodes[i]["linepos2"]
        #print(state)
        G.nodes[i]["color"] = dict(val_map).get(state)

    values = [dict(G.nodes(data="color", default="b")).get(node) for node in G.nodes()]
    nx.draw(G, node_color=values, with_labels=True, font_color='white')
    plt.show()

def initG(G,nusers):
    for i in range(nusers):
        G.nodes[i]["linepos1"] = '0' 

        G.nodes[i]["linepos2"] = '1' 

def countaFakeGood(G,nusers):
    fakenews = 0
    goodnews = 0
    for i in range(nusers):
        fakenews = fakenews + int(G.nodes[i]["linepos1"]) + int(G.nodes[i]["linepos2"])
        if(int(G.nodes[i]["linepos1"]) == 0):
            goodnews += 1
        if(int(G.nodes[i]["linepos2"]) == 0):
            goodnews += 1
    return fakenews,goodnews

def convertTimeLine(G,nusers):
    for i in range(nusers):
        tline[i] = sllist([int(G.nodes[i]["linepos1"]),int(G.nodes[i]["linepos2"])])

def ReverseConvertTimeLine(G,nusers):
    for i in range(nusers):
        G.nodes[i]["linepos1"] = str(tline[i][0])
        G.nodes[i]["linepos2"] = str(tline[i][1])
    
def countL(linkedlist,i):
    count = 0
    for value in linkedlist:
        if (value == i):
            count += 1
    return count

def addEventos(i,j,tempo,tipo):
    global globalId
    globalId += 1
    filaEventos.append(Evento(globalId,tipo,tempo,i,j))

def trataEventos():
    filaEventos.sort(key=lambda x: x.tempo, reverse=True)
        
    for obj in filaEventos:
        print(obj.id,obj.tipo,obj.tempo,obj.remetente,obj.destinatario)

def escolheOrigem():
    return int(random.choices(["0","1","2","3","4"],weights=([0.2,0.2,0.2,0.2,0.2]))[0])

def escolheDestino(a):
    weights = []
    for i in range(nusers):
        if(i != a):
          weights.append(0.25)
        else:
          weights.append(0)      
    return int(random.choices(['0','1','2','3','4'],weights)[0])

def escolheMensagem(a):
    return int(random.choices(['0','1'],weights=[countL(tline[a],0),countL(tline[a],1)])[0])

def executaSimulacao(origem,destino,tipo):
    if(tipo == 1):
       nfakes = countL(tline[origem],1)
       addEventos(origem,destino,nextArrival(alfa*nfakes)+alfa0,'fake')
    else:
       ngoods = countL(tline[origem],0)
       addEventos(origem,destino,nextArrival(mi*ngoods)+alfa1,'good') 

def countNews(tipo):
    value = 0
    for i in range(nusers):
      value += countL(tline[i],tipo)
    return value

val_map = {
           '00': "b", # blue , no fake news
           '01':"#CCCC00", # yellow , fake new at top
           '10': "#FF7F50", # orange , fake new at bottom
           '11': "r" # red , two fake news
}

tline = {} 
nusers = 5
namostras = 1000
alfa = 0.15
mi = 0.10
alfa0 = 0
alfa1 = 0
filaEventos = []
globalId = 0
taxaDeChegadas = 0.50
tempo = [0]
tempoContinuo = 0
fakeVec = []
goodVec = []

G = nx.complete_graph(nusers)
initG(G,nusers)
goodnews,fakenews = countaFakeGood(G,nusers)
convertTimeLine(G,nusers)
random = SystemRandom ()
passos = 0

#inicializa lista de eventos: sortea tempo da proxima chegada e inclui na lista de eventos
a = escolheOrigem()
executaSimulacao(a ,escolheDestino(a),escolheMensagem(a))
fakeVec.append(countNews(1))
#enquanto L != 0 ou tiver somente fakenews ou goodnews
while(countNews(1) < (nusers*2) and countNews(0) < (nusers*2) and len(filaEventos) != 0):
    #remover evento e da lista L
    evento = filaEventos.pop(0)
    #print(evento.tempo)
    if(evento.tipo == 'fake'):
        print(tline[evento.destinatario])
        tline[evento.destinatario].popleft()
        tline[evento.destinatario].append(1)
        print(tline[evento.destinatario])
    if(evento.tipo == 'good'):
        print(tline[evento.destinatario])
        tline[evento.destinatario].popleft()
        tline[evento.destinatario].append(0)
        print(tline[evento.destinatario])

    fakeVec.append(countNews(1))
    tempo.append(tempo[len(tempo)-1] + evento.tempo)

    for i in range(nusers):
        a = escolheOrigem()
        executaSimulacao(a ,escolheDestino(a),escolheMensagem(a))
    filaEventos.sort(key=lambda x: x.tempo, reverse=True)



#filaEventos.sort(key=lambda x: x.tempo, reverse=True)
#for obj in filaEventos:
#    print(obj.id,obj.tipo,obj.tempo,obj.remetente,obj.destinatario)
ReverseConvertTimeLine(G,nusers)
#plot(G,nusers)

#print(tempo)
#print(fakeVec)
#plt.plot(tempo,fakeVec)
#plt.show()



