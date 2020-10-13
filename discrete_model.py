import random as rd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
        self.coroned = self.init[5]


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
            self.coroned[random]=True #contamination


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
                if ((X[i]-X[j])**2 +(Y[i]-Y[j])**2)**(1/2)<e:
                    if self.coroned[i] or self.coroned[j]:
                        self.coroned[i],self.coroned[j]=True,True
        self.x,self.y=X,Y
    

    def reset(self):
        """réinitialise la population à partir de la liste init"""
        self.x=self.init[0]
        self.x=self.init[1]
        self.vx=self.init[2]
        self.vx=self.init[3]
        self.coroned=[False for i in range(self.n)]


def animer(P,frames=1000,fr=1/60,m=0.15,e=1): 
    """animation (calcul entre deux affichages) qui fonctionne pour une petite population"""
    anim,=plt.plot(P.x,P.y,'.')
    plt.xlim(0,P.r)
    plt.ylim(0,P.r)
    for i in range(frames):
        P.propagation(m,e)
        anim.set_xdata(P.x)
        anim.set_ydata(P.x)
        plt.pause(fr)
    plt.show()

def animer_pre(P,frames=1000,fr=1/60,m=0.15,e=1):
    """animation d'une population (fait tous les calculs avant d'animer pour avoir un animation plus fluide sur une grande population)"""
    anim,=plt.plot(P.x,P.y,'.') #crée la figure
    plt.xlim(0,P.r) #place les limite du graph
    plt.ylim(0,P.r)
    X,Y,C=simulation(P,frames,m,e)
    for i in range(frames):
        anim.set_xdata(X[i]) #ajoute les données instant après instant dans l'animation
        anim.set_ydata(Y[i])
        plt.pause(fr)  #définit les la fréquence d'affichage en déterminant la période de pause entre deux graphiques.
    plt.show()

def animation_coroned(P,duree=1000,fr=1/60,pas=0.15,e=1):
    """évolution des personnes contaminées"""
    anim,=plt.plot([],[])
    plt.xlim(0,duree)
    plt.ylim(0,P.n)
    X,Y,C=simulation(P,duree,pas,e)
    for i in range(duree):
        anim.set_xdata([j for j in range(i)])
        anim.set_ydata([sum(C[j]) for j in range(i)])
        plt.pause(fr)
    plt.show()


def animergold(P,frames=1000,fr=1/60,m=0.15,e=1): 
    """animation (calcul entre deux affichages) qui fonctionne pour une petite population"""
    fig,_=plt.subplots()

    plt.subplot(1,2,1)
    anim_move,=plt.plot(P.x,P.y,'.')
    anim_move2,=plt.plot([],[],'.')
    plt.xlim(0,P.r)
    plt.ylim(0,P.r)
    X,Y,C=simulation(P,frames,m,e)

    plt.subplot(1,2,2)
    anim_graph,=plt.plot([],[]) #crée la figure
    plt.xlim(0,frames)
    plt.ylim(0,P.n)

    def animer_Func(i):
        anim_move.set_data(X[i],Y[i])
        anim_move2.set_data(X[i-2],Y[i-2])
        anim_graph.set_data([j for j in range(i)],[sum(C[j]) for j in range(i)])
        return anim_move,anim_move2,anim_graph
    
    ani = animation.FuncAnimation(fig=fig, func=animer_Func, frames=range(frames), interval=10, blit=True)
    plt.show()
    # ani.save(filename="courbe.mp4", dpi =80, fps=20)


def simulation(P,duree,pas,e):
    """fait la simulation de la population P sur une certaine duree"""
    X,Y,C=[],[],[]
    for i in range(duree):
        P.propagation(pas,e) #fait chaque calcul de propagation
        X+=[[x for x in P.x]] #récupère la position de chaque point entre chaque déplacement
        Y+=[[y for y in P.y]]
        C+=[[b for b in P.coroned]]
    return X,Y,C

#faire plusieurs anim de différentes couleurs indépendantes entre elles.

P=population(100,50)
P.contaminer()
animergold(P,1000,0.001,0.1)
breakpoint()