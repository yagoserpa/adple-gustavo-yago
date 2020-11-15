import numpy as np
import itertools
import biblioteca as bib
import scipy.linalg as la
import matplotlib.pyplot as plt
import simula

nusers = 5
lambda0=0
lambda1=0
rate1 = 1
rate2 = 2

states_map = {
           '00': "color1", # blue , no fake news
           '01': "color2", # orange , fake new at bottom
           '10': "color3", # yellow , fake new at top
           '11': "color4" # red , two fake news
}

array = list(states_map.values()) * nusers
states = bib.perms(array,nusers)

#print(states)
states_number = []

for i in range(len(states)):
    states_number.append([states[i].count("color1"),states[i].count("color2"),states[i].count("color3"),states[i].count("color4")])

states_number= sorted(states_number,reverse=1)
def mergeString(list):
    word = ''.join(str(x) for x in list)
    return word
    

dict = {mergeString(tuple(key)): idx for idx, key in enumerate(states_number)}

nstates = len(states_number)
Q = np.zeros((nstates,nstates))

for i in range(nstates):
    curstate = states_number[i]
    if(curstate[0]>0): # 00 === receive fake news ===> 01
        nextstate = curstate.copy()
        nextstate[0] =  curstate[0] - 1
        nextstate[1] =  nextstate[1] + 1
        idnextstate = dict[mergeString(nextstate)]
        Q[i][idnextstate] = curstate[0] * (((curstate[1]+curstate[2])*rate1) + curstate[3]*rate2 + lambda1)

    if(curstate[0]>0): # 00 === receive fake news ===> 10
        nextstate = curstate.copy()
        nextstate[0] =  curstate[0] - 1
        nextstate[2] =  nextstate[2] + 1
        idnextstate = dict[mergeString(nextstate)]
        Q[i][idnextstate] = curstate[0] * (((curstate[1]+curstate[2])*rate1) + curstate[3]*rate2 + lambda1)


    if(curstate[1]>0): # 01 === receive fake news ===> 11
        nextstate = curstate.copy()
        nextstate[1] =  curstate[1] - 1
        nextstate[3] =  nextstate[3] + 1
        idnextstate = dict[mergeString(nextstate)]
        Q[i][idnextstate] = ( curstate[1] * (((curstate[1]-1+curstate[2])*rate1) + curstate[3]*rate2 + lambda1) )
  
        
    if(curstate[1]>0): # 01 === receive good news ===> 00
        nextstate = curstate.copy()
        nextstate[1] =  curstate[1] - 1
        nextstate[0] =  nextstate[0] + 1
        idnextstate = dict[mergeString(nextstate)]
        Q[i][idnextstate] = curstate[1] * (((curstate[1]-1+curstate[2])*rate1) + curstate[0]*rate2 + lambda0)


    if(curstate[2]>0): #10 receive fake news ====> 11
        nextstate = curstate.copy()
        nextstate[2] =  curstate[2] - 1
        nextstate[3] =  nextstate[3] + 1
        idnextstate = dict[mergeString(nextstate)]
        Q[i][idnextstate] = curstate[2] * (((curstate[1]+curstate[2]-1)*rate1) + curstate[3]*rate2 + lambda1)
 
    if(curstate[2]>0): #10 receive good news ====> 00
        nextstate = curstate.copy()
        nextstate[2] =  curstate[2] - 1
        nextstate[0] =  nextstate[0] + 1
        idnextstate = dict[mergeString(nextstate)]
        Q[i][idnextstate] = curstate[2] * (((curstate[1]+curstate[2]-1)*rate1) + curstate[0]*rate2 + lambda0)

    if(curstate[3]>0): # 11 === receive good news ====> 10
        nextstate = curstate.copy()
        nextstate[3] =  curstate[3] - 1
        nextstate[2] =  nextstate[2] + 1
        idnextstate = dict[mergeString(nextstate)]
        Q[i][idnextstate] = curstate[3] * (((curstate[1]+curstate[2])*rate1) + curstate[0]*rate2 + lambda0)
     
    if(curstate[3]>0): # 11 === receive good news ====> 01
        nextstate = curstate.copy()
        nextstate[3] =  curstate[3] - 1
        nextstate[1] =  nextstate[1] + 1
        idnextstate = dict[mergeString(nextstate)]
        Q[i][idnextstate] = curstate[3] * (((curstate[1]+curstate[2])*rate1) + curstate[0]*rate2 + lambda0)
        
   

for i in range(nstates):
    Q[i][i] = -Q[i].sum(axis=0)

inival = 0.01
inc = 0.01
maxt = 6
initstate = 35

interval = np.linspace(inival,maxt,600)
transient = np.zeros((len(interval),nstates))

for index, t in enumerate(interval):
    trans = la.expm(Q * t)
    transient[index] = trans[initstate]

plt.plot(interval,transient[:,nstates-1],'b--' , label = "state (0 0 0 5): all fake")
plt.plot(interval,transient[:,0],'r', label = "state (5 0 0 0): all non fake")
plt.legend(loc="best")
plt.xlabel('Time')
plt.ylabel('State Probability')

plt.show()

state,goodVec,fakeVec = simula.simula_eventos_discretos(Q,120,0,1000)
print("Média Probabilidade do Estado All Non Fake {}".format(np.mean(goodVec)))
print("Variancia Probabilidade do Estado All Non Fake {}".format(np.var(goodVec)))
confinteru=np.mean(goodVec)+1.96*(np.std(goodVec)/np.sqrt(len(goodVec)))
confinterl=np.mean(goodVec)-1.96*(np.std(goodVec)/np.sqrt(len(goodVec)))
print("IC superior Probabilidade do Estado All Non Fake {}".format(confinteru))
print("IC inferior Probabilidade do Estado All Non Fake {}".format(confinterl))
print("\n")
print("Média Probabilidade do Estado All Fake {}".format(np.mean(fakeVec)))
print("Variancia Probabilidade do Estado All Fake {}".format(np.var(fakeVec)))
confinteru=np.mean(fakeVec)+1.96*(np.std(fakeVec)/np.sqrt(len(fakeVec)))
confinterl=np.mean(fakeVec)-1.96*(np.std(fakeVec)/np.sqrt(len(fakeVec)))
print("IC superior Probabilidade do Estado All Fake {}".format(confinteru))
print("IC inferior Probabilidade do Estado All Fake {}".format(confinterl))

#state = simulaRND.simula_eventos_discretos(Q)
#print(state)