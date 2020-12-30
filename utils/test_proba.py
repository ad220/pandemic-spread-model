from math import cos,sin,pi
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import csv

def proba(n,r,précision,π=-1):
    PI=round(π*n)
    positions=np.array([[rd.random()*r for i in range(n)],[rd.random()*r for i in range(n)]])
    vX,vY=[],[]
    for _ in range(n):
        direction=rd.random()*2*pi
        vX+=[cos(direction)]
        vY+=[sin(direction)] 
    vitesses=np.array([vX,vY])
    if π==-1: n_personnes_rencontrées=[0 for _ in range(n)]
    else: n_personnes_rencontrées=[0 for _ in range(PI)]

    for _ in range(précision):
        if π==-1:
            for i in range(n-1):
                for j in range(i+1,n):
                    if ((positions[0][i]-positions[0][j])**2 +(positions[1][i]-positions[1][j])**2)**(1/2)<=1:
                        n_personnes_rencontrées[i]+=1
                        n_personnes_rencontrées[j]+=1
        else:
            for i in range(PI):
                for j in range(PI,n):
                    if ((positions[0][i]-positions[0][j])**2 +(positions[1][i]-positions[1][j])**2)**(1/2)<=1:
                        n_personnes_rencontrées[i]+=1

        positions=positions+0.2*vitesses
        for p in range(n):
            if positions[0][p] > r :       positions[0][p] , vitesses[0][p]  =  2*r-positions[0][p] , -vitesses[0][p]
            elif positions[0][p] < 0 :     positions[0][p] , vitesses[0][p]  =  -positions[0][p] , -vitesses[0][p]
            if positions[1][p] > r :       positions[1][p] , vitesses[1][p]  =  2*r-positions[1][p] , -vitesses[1][p]
            elif positions[1][p] < 0 :     positions[1][p] , vitesses[1][p]  =  -positions[1][p] , -vitesses[1][p]

    if π==-1: return sum(n_personnes_rencontrées)/(n*précision)
    return sum(n_personnes_rencontrées)/précision


def plot_proba(nMax,r,précision=1000):
    N=[n for n in range(1,nMax+1)]
    # P=[proba(n,r,précision) for n in N]
    P=[]
    for n in N:
        P+=[proba(n,r,précision)]
        print(n*100/nMax)
    # plt.plot(N,P)
    # plt.show()
    return N,P

def plot_proba_into_csv(nMax,r,précision=1000):
    fichierCsv=open('proba.csv','w')
    écriveur=csv.writer(fichierCsv)

    for n in range(1,nMax+1):
        écriveur.writerow(proba(n,r,précision))
        print(n*100/nMax)
    
    fichierCsv.close()

def plot_from_csv(nomCsv):
    fichierCsv=open(nomCsv,'r')
    lecteur=csv.reader(fichierCsv)
    P=[proba for proba in lecteur]
    fichierCsv.close()
    plt.plot([n for n in range(1,len(P)+1)],P)
    plt.show()

def write_to_csv(liste,nomCsv='liste.csv'):
    fichier=open(nomCsv,'w')
    écriveur=csv.writer(fichier)
    for e in liste: écriveur.writerow(e)
    fichier.close()

def plot_proba_FAST(nMin,nMax,r,précision=100):
    R=[r*(nMin/(nMin+n))**(1/2) for n in range(nMax-nMin+1)]
    P=[]
    for i in range(len(R)):
        P+=[proba(nMin,R[i],précision)]
        print(i*100/len(R))
    # plt.plot([n for n in range(nMin,nMax+1)],P)
    # plt.show()
    return [n for n in range(nMin,nMax+1)],P

def plotDuo(nMin,nMax,r,précision=100):
    N,R=plot_proba_FAST(nMin,nMax,r,précision*10)
    plt.plot(N,R)
    N,R=plot_proba(nMax,r,précision)
    plt.plot(N,R)
    plt.show()


# plot_proba_FAST(10,1000,1000**(1/2))
r_mille=(100*pi)**(1/2)
print(proba(500,80,100))
# plot_from_csv('proba.csv')
# plotDuo(10,200,32,50)