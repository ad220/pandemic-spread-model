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
        self.infectés = []
        self.sains = [i for i in range(n)]
        

    def __repr__(self):
        """représente la position de tous les éléments de la population sur un graph"""
        plt.plot([self.x[i] for i in self.sains],[self.y[i] for i in self.sains],'.',color="green")
        plt.plot([self.x[i] for i in self.infectés],[self.y[i] for i in self.infectés],'.',color="red")
        plt.xlim(0,self.r)
        plt.ylim(0,self.r)
        plt.show()


    def contaminer_old(self,n=1):
        """Contamine n éléments dans la population"""
        pool=[-1] #Initialise la liste des éléments déjà contaminés pour pas contaminer deux fois la même personne
        for i in range(n):
            random=-1 #un élément déjà dans pool pour entrer dans la boucle while
            while random in pool: #on vérifie que l'élément choisi n'a pas déjà été contaminé
                random=rd.randint(0,self.n-1) #élément aléatoire
            pool+=[random]
            self.malade[random]=True #contamination
            self.infectés+=[random]
            self.sains.remove(random)

    def contaminer(self,n=1):
        """Contamine n éléments dans la population"""
        for i in range(n):
            self.malade[i]=True #contamination
            self.infectés+=[i]
            self.sains.remove(i)


    def propagation(self,m=0.1,e=1):
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

        for i in self.infectés: #on vérifie si les éléments sont trop proches deux à deux (complexité en n!)
            for j in self.sains:
                if rd.random()<self.proba and ((X[i]-X[j])**2 +(Y[i]-Y[j])**2)**(1/2)<e and self.timer[j]>0:
                        self.malade[j]=True
                        self.infectés+=[j]
                        self.sains.remove(j)

        for i in range(self.n):
            if self.timer[i]==0:
                self.malade[i]=False
                self.sains+=[i]
                self.infectés.remove(i)
                self.timer[i]=-1
            elif self.malade[i]:
                self.timer[i]-=1

        self.x,self.y=X,Y
    

    def reset(self):
        """réinitialise la population à partir de la liste init"""
        self.x=self.init[0]
        self.x=self.init[1]
        self.vx=self.init[2]
        self.vx=self.init[3]
        self.malade=[False for i in range(self.n)]

def copy(objet): return [e for e in objet]

def simulation(P,duree,pas,e,temps_guerison,proba,echo=False):
    """fait la simulation de la population P sur une certaine duree"""
    X,Y,C,S,I=[P.x],[P.y],[P.malade],[P.sains],[P.infectés]
    P.timer=[temps_guerison for i in range(P.n)]
    P.proba=proba
    for i in range(duree-1):
        P.propagation(pas,e) #fait chaque calcul de propagation
        X+=[copy(P.x)] #récupère la position de chaque point entre chaque déplacement
        Y+=[copy(P.y)]
        C+=[copy(P.malade)]
        S+=[copy(P.sains)]
        I+=[copy(P.infectés)]
        print(str(100*(i+1)/duree)+"%")
    return X,Y,C,S,I


def animation(P,frames=1000,fr=1/60,m=0.15,e=1,tg=-1,proba=1): 
    plt.subplot(1,2,1)
    anim_sains,=plt.plot([],[],'.',color="green")
    anim_infectés,=plt.plot([],[],'.',color="red")

    plt.xlim(0,P.r)
    plt.ylim(0,P.r)
    X,Y,C,S,I=simulation(P,frames,m,e,tg,proba)

    plt.subplot(1,2,2)
    anim_graph,=plt.plot([],[]) #crée la figure
    plt.xlim(0,frames)
    plt.ylim(0,P.n)

    for i in range(frames):
        anim_sains.set_xdata([X[i][j] for j in S[i]])
        anim_sains.set_ydata([Y[i][j] for j in S[i]])
        anim_infectés.set_xdata([X[i][j] for j in I[i]])
        anim_infectés.set_ydata([Y[i][j] for j in I[i]])
        anim_graph.set_xdata([j for j in range(i)])
        anim_graph.set_ydata([sum(C[j]) for j in range(i)])
        plt.pause(fr)
    plt.show()

def graph(P,duree=1000,pas=0.15,e=1,temps_guerison=-1,proba=1):
    _,_,C,_,_=simulation(P,duree,pas,e,temps_guerison,proba)
    coroned=[sum(C[t]) for t in range(duree)]
    plt.plot([t for t in range(duree)],coroned)
    plt.show()


#faire plusieurs anim de différentes couleurs indépendantes entre elles.

P=population(5000,800)
P.contaminer(5)
animation(P,10000,1/60,0.2,2,200,1/3)
#graph(P,1000,0.2,1,200,1/3)
