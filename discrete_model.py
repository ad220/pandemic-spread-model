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
        self.malade = self.init[5]
        self.timer = [-1 for i in range(n)]
        self.proba = 1


    def __repr__(self):
        """représente la position de tous les éléments de la population sur un graph"""
        plt.plot(self.x,self.y,'.')
        plt.xlim(0,self.r)
        plt.ylim(0,self.r)
        plt.show()


    def contaminer(self,n=1):
        """Contamine n éléments dans la population"""
        pool=[-1] #Initialise la liste des éléments déjà contaminés pour pas contaminer deux fois la même personne
        for i in range(n):
            random=-1 #un élément déjà dans pool pour entrer dans la boucle while
            while random in pool: #on vérifie que l'élément choisi n'a pas déjà été contaminé
                random=rd.randint(0,self.n) #élément aléatoire
            pool+=[random]
            self.malade[random]=True #contamination


    def propagation(self,m=1,e=1):
        """Fait se déplacer chaque élément d'un déplacement m et vérifie si deux éléments sont susceptible de se contaminer leur distance relative < e"""
        b=self.r
        X,Y,vX,vY=self.x,self.y,self.vx,self.vy
        X=[X[i]+m*vX[i] for i in range(self.n)] #Chaque point se déplace de m selon sa trajectoire (sur x)
        Y=[Y[i]+m*vY[i] for i in range(self.n)] # ... de même sur y

        for i in range(self.n): #On vérifie que les éléments sont toujours dans l'espace d'étude sinon ils "rebondissent"
            if X[i] > b :       X[i] , vX[i]  =  b , -vX[i]
            elif X[i] < 0 :     X[i] , vX[i]  =  0 , -vX[i]
            if Y[i] > b :       Y[i] , vY[i]  =  b , -vY[i]
            elif Y[i] < 0 :     Y[i] , vY[i]  =  0 , -vY[i]

        for i in range(self.n-1): #on vérifie si les éléments sont trop proches deux à deux (complexité en n!)
            for j in range(i+1,self.n):
                if ((X[i]-X[j])**2 +(Y[i]-Y[j])**2)**(1/2)<e and rd.random()<self.proba:
                    if self.malade[i] and self.timer[j]>0: self.malade[j]=True
                    if self.malade[j] and self.timer[i]>0: self.malade[i]=True
        
        for i in range(self.n):
            if self.timer[i]==0:
                self.malade[i]=False
            if self.malade[i]:
                self.timer[i]-=1

        self.x,self.y=X,Y
    

    def reset(self):
        """réinitialise la population à partir de la liste init"""
        self.x=self.init[0]
        self.x=self.init[1]
        self.vx=self.init[2]
        self.vx=self.init[3]
        self.malade=[False for i in range(self.n)]


def simulation(P,duree,pas,e,temps_guerison,proba):
    """fait la simulation de la population P sur une certaine duree"""
    X,Y,C=[P.x],[P.y],[P.malade]
    P.timer=[temps_guerison for i in range(P.n)]
    P.proba=proba
    for i in range(duree-1):
        P.propagation(pas,e) #fait chaque calcul de propagation
        X+=[[x for x in P.x]] #récupère la position de chaque point entre chaque déplacement
        Y+=[[y for y in P.y]]
        C+=[[b for b in P.malade]]
    return X,Y,C


def animation(P,frames=1000,fr=1/60,m=0.15,e=1,tg=-1,proba=1): 
    """animation (calcul entre deux affichages) qui fonctionne pour une petite population"""
    plt.subplot(1,2,1)
    anim_move,=plt.plot(P.x,P.y,'.')
    plt.xlim(0,P.r)
    plt.ylim(0,P.r)
    X,Y,C=simulation(P,frames,m,e,tg,proba)

    plt.subplot(1,2,2)
    anim_graph,=plt.plot([],[]) #crée la figure
    plt.xlim(0,frames)
    plt.ylim(0,P.n)

    for i in range(frames):
        anim_move.set_xdata(X[i])
        anim_move.set_ydata(Y[i])
        anim_graph.set_xdata([j for j in range(i)])
        anim_graph.set_ydata([sum(C[j]) for j in range(i)])
        plt.pause(fr)
    plt.show()

def graph(P,duree=1000,pas=0.15,e=1,temps_guerison=-1,proba=1):
    X,Y,C=simulation(P,duree,pas,e,temps_guerison,proba)
    coroned=[sum(C[t]) for t in range(duree)]
    plt.plot([t for t in range(duree)],coroned)
    plt.show()




#faire plusieurs anim de différentes couleurs indépendantes entre elles.

P=population(500,100)
P.contaminer()
#animation(P,1500,0.001,0.15,1,200)
graph(P,10000,0.2,1,200,1/3)
breakpoint()


#Proba contamination
#Contaminé --> Guéri (immune)
