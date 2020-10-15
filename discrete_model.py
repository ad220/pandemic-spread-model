import random as rd
import matplotlib.pyplot as plt
from math import *

class population(object):
    def __init__(self,n,r):
        """Crée une population de n individus, de direction donnée, dans un espace carré de coté r"""
        pop=[[rd.randint(0,r) for i in range(n)],[rd.randint(0,r) for i in range(n)]] #Position de chaque point
        vx,vy=[],[]
        for i in range(n):
            direction=rd.random()*2*pi #Direction aléatoire
            vx+=[cos(direction)] #Direction selon x
            vy+=[sin(direction)] #Direction selon y
        self.init = pop+[vx,vy,[r],[False for i in range(n)]]
        self.n = n
        self.r = r
        self.x = pop[0]
        self.y = pop[1]
        self.vx = vx
        self.vy = vy
        self.timer = [-1 for i in range(n)]
        self.proba_infection = 1
        self.proba_mort = 0
        self.infectés = []
        self.sains = [i for i in range(n)]
        self.rétablis = []
        self.morts = []
        

    def __repr__(self):
        """représente la position de tous les éléments de la population sur un graph"""
        plt.plot([self.x[i] for i in self.sains],[self.y[i] for i in self.sains],'.',color="green")
        plt.plot([self.x[i] for i in self.infectés],[self.y[i] for i in self.infectés],'.',color="red")
        plt.plot([self.x[i] for i in self.rétablis],[self.y[i] for i in self.rétablis],'.',color="orange")
        plt.plot([self.x[i] for i in self.morts],[self.y[i] for i in self.morts],'.',color="grey")
        plt.xlim(0,self.r)
        plt.ylim(0,self.r)
        plt.show()

    def contaminer(self,n=1):
        """Contamine n éléments dans la population"""
        for i in range(n):
            self.infectés+=[i]
            self.sains.remove(i)

    def propagation(self,m,e):
        """Fait se déplacer chaque élément d'un déplacement m et vérifie si deux éléments sont susceptible de se contaminer leur distance relative < e"""
        b=self.r
        X,Y,vX,vY=self.x,self.y,self.vx,self.vy
        for i in range(self.n):
            if i in self.sains+self.infectés+self.rétablis:
                X[i]+=m*vX[i]
                Y[i]+=m*vY[i]

        for i in range(self.n): #On vérifie que les éléments sont toujours dans l'espace d'étude sinon ils "rebondissent"
            if X[i] > b :       X[i] , vX[i]  =  b , -vX[i]
            elif X[i] < 0 :     X[i] , vX[i]  =  0 , -vX[i]
            if Y[i] > b :       Y[i] , vY[i]  =  b , -vY[i]
            elif Y[i] < 0 :     Y[i] , vY[i]  =  0 , -vY[i]

        for i in self.infectés: #on vérifie si les éléments sont trop proches deux à deux (complexité en n!)
            for j in self.sains:
                if rd.random()<self.proba_infection and ((X[i]-X[j])**2 +(Y[i]-Y[j])**2)**(1/2)<e:
                        self.infectés+=[j]
                        self.sains.remove(j)

        for i in range(self.n):
            if self.timer[i]==0:
                self.rétablis+=[i]
                self.infectés.remove(i)
                self.timer[i]=-1
            elif i in self.infectés:
                if rd.random()<self.proba_mort:
                    self.infectés.remove(i)
                    self.morts+=[i]
                self.timer[i]-=1

        self.x,self.y=X,Y
    

    def reset(self):
        """réinitialise la population à partir de la liste init"""
        self.x=self.init[0]
        self.x=self.init[1]
        self.vx=self.init[2]
        self.vx=self.init[3]

def copy(objet): return [e for e in objet]

def simulation(P,duree,pas,e,temps_guerison,proba_infection,proba_mort):
    """fait la simulation de la population P sur une certaine duree"""
    X,Y,S,I,R,M=[copy(P.x)],[copy(P.y)],[copy(P.sains)],[copy(P.infectés)],[copy(P.rétablis)],[copy(P.morts)]
    P.timer=[temps_guerison for i in range(P.n)]
    P.proba_infection=proba_infection
    P.proba_mort=proba_mort
    for i in range(duree-1):
        P.propagation(pas,e) #fait chaque calcul de propagation
        X+=[copy(P.x)] #récupère la position de chaque point entre chaque déplacement
        Y+=[copy(P.y)]
        S+=[copy(P.sains)]
        I+=[copy(P.infectés)]
        R+=[copy(P.rétablis)]
        M+=[copy(P.morts)]
        print(str(100*(i+1)/duree)+"%")
    return X,Y,S,I,R,M


def animation(P,frames=1000,fr=1/60,m=0.15,e=1,tg=-1,proba_infection=1,proba_mort=0): #changer proba_mort : recalculer en fonction de temps de duree étude
    plt.subplot(1,2,1)
    anim_sains,=plt.plot([],[],'.',color="green")
    anim_infectés,=plt.plot([],[],'.',color="red")
    anim_rétablis,=plt.plot([],[],'.',color="orange")
    anim_morts,=plt.plot([],[],'.',color="grey")

    plt.xlim(0,P.r)
    plt.ylim(0,P.r)
    X,Y,S,I,R,M=simulation(P,frames,m,e,tg,proba_infection,proba_mort)

    plt.subplot(1,2,2)
    anim_graph,=plt.plot([],[]) #crée la figure
    plt.xlim(0,frames)
    plt.ylim(0,P.n)

    for i in range(frames):
        anim_sains.set_xdata([X[i][j] for j in S[i]])
        anim_sains.set_ydata([Y[i][j] for j in S[i]])
        anim_infectés.set_xdata([X[i][j] for j in I[i]])
        anim_infectés.set_ydata([Y[i][j] for j in I[i]])
        anim_rétablis.set_xdata([X[i][j] for j in R[i]])
        anim_rétablis.set_ydata([Y[i][j] for j in R[i]])
        anim_morts.set_xdata([X[i][j] for j in M[i]])
        anim_morts.set_ydata([Y[i][j] for j in M[i]])
        anim_graph.set_xdata([j for j in range(i)])
        anim_graph.set_ydata([len(I[j]) for j in range(i)])
        plt.pause(fr)
    plt.show()

def graph(P,duree=1000,pas=0.15,e=1,temps_guerison=-1,proba=1):
    _,_,C,_,_=simulation(P,duree,pas,e,temps_guerison,proba)
    coroned=[sum(C[t]) for t in range(duree)]
    plt.plot([t for t in range(duree)],coroned)
    plt.show()


#faire plusieurs anim de différentes couleurs indépendantes entre elles.

P=population(500,80)
P.contaminer(5)
animation(P,100,1/60,0.2,2,200,1,0.005)
#graph(P,1000,0.2,1,200,1)
breakpoint()
