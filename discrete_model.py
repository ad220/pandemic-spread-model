import random as rd
import matplotlib.pyplot as plt
from math import *

def initier_population(n,r=1000):
    """Crée une population de n individus, de direction donnée (à passer enn programmation orientée objet)"""
    pop=[[rd.randint(0,r) for i in range(n)],[rd.randint(0,r) for i in range(n)]] #Position de chaque point
    x,y=[],[]
    for i in range(n):
        direction=rd.random()*2*pi #Direction aléatoire
        x+=[cos(direction)] #Direction selon x
        y+=[sin(direction)] #Direction selon y
    return pop+[x,y,[r],[False for i in range(n)]] #On ajoute la taille de l'espace de simulation et l'indicateur pour savoir si un individu est contaminé ou pas

def contaminer_population(P,n=1):
    """Contamine n éléments dans la population P"""
    pool=[-1] #Initialise la liste des éléments déjà contaminés pour pas contaminer deux fois la même personne
    npop=len(P[0])-1
    for i in range(n):
        random=-1 #un élément déjà dans pool pour entrer dans la boucle while
        while random in pool: #on vérifie que l'élément choisi n'a pas déjà été contaminé
            random=rd.randint(0,npop) #élément aléatoire
        pool+=[random]
        P[5][random]=True #contamination



def afficher_population(P):
    """Ne fonctionne plus"""
    X,Y=[],[]
    for p in P:
        x,y,=p
        X+=[x]
        Y+=[y]
    plt.plot(X,Y,'.')
    plt.show()


def propagation(P,m=1,e=1):
    """Fait se déplacer chaque élément d'un déplacement m et vérifie si deux éléments sont susceptible de se contaminer leur distance relative < e"""
    b=P[4][0] #On récupère la taille de l'espace de déplacement
    P[0]=[P[0][i]+m*P[2][i] for i in range(len(P[0]))] #Chaque point se déplace de m selon sa trajectoire (sur x)
    P[1]=[P[1][i]+m*P[3][i] for i in range(len(P[1]))] # ... de même sur y
    for i in range(len(P[0])): #On vérifie que les éléments sont toujours dans l'espace d'étude sinon ils "rebondissent"
        if P[0][i] > b :
            P[0][i]=b
            P[2][i]=-P[2][i]
        elif P[0][i] < 0 :
            P[0][i]=0
            P[2][i]=-P[2][i]

        if P[1][i] > b :
            P[1][i]=b
            P[3][i]=-P[3][i]
        elif P[1][i] < 0 :
            P[1][i]=0
            P[3][i]=-P[3][i]

    for i in range(len(P[0])-1): #on vérifie si les éléments sont trop proches deux à deux (complexité en n!)
        for j in range(i+1,len(P[0])):
            if ((P[0][i]-P[0][j])**2 +(P[1][i]-P[1][j])**2)**(1/2)<e:
                if P[5][i] or P[5][j]:
                    P[5][i],P[5][j]=True,True
    
    








def animer(P,m=0.15,frames=1000,fr=0.001): #animation (calcul entre deux affichages) qui fonctionne pour une petite population
    anim,=plt.plot(P[0],P[1],'.')
    plt.xlim(0,P[4][0])
    plt.ylim(0,P[4][0])
    for i in range(frames):
        propagation(P,m)
        anim.set_xdata(P[0])
        anim.set_ydata(P[1])
        plt.pause(fr)
    plt.show()

def animer_pre(P,frames=1000,fr=0.01,m=0.15,e=1): #animation d'une population (fait tous les calculs avant d'animer pour avoir un animation plus fluide sur une grande population)
    anim,=plt.plot(P[0],P[1],'.') #crée la figure
    plt.xlim(0,P[4][0]) #place les limite du graph
    plt.ylim(0,P[4][0])
    X,Y=[],[]
    for i in range(frames):
        propagation(P,m,e) #fait chaque calcul de propagation
        X+=[[x for x in P[0]]] #récupère la position de chaque point entre chaque déplacement
        Y+=[[y for y in P[1]]]
    for i in range(frames):
        anim.set_xdata(X[i]) #ajoute les données instant après instant dans l'animation
        anim.set_ydata(Y[i])
        plt.pause(fr)  #définit les la fréquence d'affichage en déterminant la période de pause entre deux graphiques.
    plt.show()

#faire plusieurs anim de différentes couleurs indépendantes entre elles.

P=initier_population(100,50)
contaminer_population(P)
animer_pre(P,100)
breakpoint()