import random as rd
import csv
import matplotlib.pyplot as plt
from math import *

class population(object):
    def __init__(self,n=0,r=0):
        """Crée une population de n individus, de direction donnée, dans un espace carré de coté r"""
        pop=[[rd.randint(0,r) for i in range(n)],[rd.randint(0,r) for i in range(n)]] #Position de chaque point
        vx,vy=[],[] #Direction de chaque point selon x et y
        for i in range(n):
            direction=rd.random()*2*pi #Direction aléatoire
            vx+=[cos(direction)] #direction selon x
            vy+=[sin(direction)] #direction selon y
        self.n = n #nombre d'individus
        self.r = r #taille de l'étude
        self.x = pop[0] #coordonnées sur x
        self.y = pop[1] #coordonnées sur y
        self.vx = vx #direction selon x
        self.vy = vy #direction selon y
        self.timer = [-1 for i in range(n)] #temps avant guérison (initié à 1)
        self.sains = [i for i in range(n)] #indices des individus sains
        self.infectés = [] #... infectés
        self.rétablis = [] #... rétablis
        self.morts = [] #... décédés
        self.immunisés = [] #... immunisés (pas après la maladie mais de façon acquise)

    def __repr__(self): #Représente la position des tous les éléments sur un graphique
        """représente la position de tous les éléments de la population sur un graph"""
        plt.plot([self.x[i] for i in self.sains],[self.y[i] for i in self.sains],'.',color="green") #On représentera toujours les sains en vert,
        plt.plot([self.x[i] for i in self.infectés],[self.y[i] for i in self.infectés],'.',color="red") #les infectés en rouge,
        plt.plot([self.x[i] for i in self.rétablis],[self.y[i] for i in self.rétablis],'.',color="orange") #les rétablis en jaune (orangé),
        plt.plot([self.x[i] for i in self.morts],[self.y[i] for i in self.morts],'.',color="grey") #les morts en noir (ne bougent plus),
        plt.plot([self.x[i] for i in self.immunisés],[self.y[i] for i in self.immunisés],'.',color="blue") #les immunisés en bleus (et restent toujours en bleu donc).
        plt.xlim(0,self.r) #On définit la taille de l'étude maximale sur x
        plt.ylim(0,self.r) # et sur y.
        plt.show()

    def contaminer(self,n=1): #Contamine les n premiers éléments sains de la population (reste aléatoire car leur position l'est)
        """Contamine n éléments dans la population"""
        i=0
        for _ in range(n):
            while not i in self.sains:
                i+=1
            self.infectés+=[i]
            self.sains.remove(i)

    def immuniser(self,n=0): #Immunise les n premiers éléments sains de la population
        """Immunise n éléments dans la population"""
        i=0
        for _ in range(n):
            while not i in self.sains:
                i+=1
            self.immunisés+=[i]
            self.sains.remove(i)

    def propagation(self,pas,rayon_propagation,proba_infection,proba_mort): #Propage l'épidémie à l'instant suivant
        """Fait se déplacer chaque élément d'un déplacement m et vérifie si deux éléments sont susceptible de se contaminer leur distance relative < e"""
        b=self.r #on récupère la taille de l'espace
        X,Y,vX,vY=self.x,self.y,self.vx,self.vy #et les différentes caractéristiques de la population
        for i in range(self.n):
            if i in self.sains+self.infectés+self.rétablis+self.immunisés: #On fait déplace tous les individus vivants selon leur direction d'une distance unitaire (pas)
                X[i]+=pas*vX[i]
                Y[i]+=pas*vY[i]

        for i in range(self.n): #On vérifie que les éléments sont toujours dans l'espace d'étude sinon ils "rebondissent"
            if X[i] > b :       X[i] , vX[i]  =  b , -vX[i]
            elif X[i] < 0 :     X[i] , vX[i]  =  0 , -vX[i]
            if Y[i] > b :       Y[i] , vY[i]  =  b , -vY[i]
            elif Y[i] < 0 :     Y[i] , vY[i]  =  0 , -vY[i]

        for i in self.infectés: #Si un élément sain et un autre infecté dont trop proches entre eux, ils ont une probabilité proba_infection de se contaminer
            for j in self.sains:
                if rd.random()<proba_infection and ((X[i]-X[j])**2 +(Y[i]-Y[j])**2)**(1/2)<rayon_propagation:
                        self.infectés+=[j]
                        self.sains.remove(j)

        for i in self.infectés:
            if self.timer[i]==0: #On guérit les individus ayant fini leur période d'infection
                self.rétablis+=[i]
                self.infectés.remove(i)
            elif rd.random()<proba_mort: #Chaque infecté a une probabilité proba_mort de mourrir à chaque instant
                self.infectés.remove(i)
                self.morts+=[i]
            self.timer[i]-=1

        self.x,self.y=X,Y


def copy(objet): return [e for e in objet] #Copie d'une liste

def simulation(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort):
    """Fait la simulation de la population P sur une certaine duree selon certaines données"""
    X,Y,S,I,R,M,N=[copy(P.x)],[copy(P.y)],[copy(P.sains)],[copy(P.infectés)],[copy(P.rétablis)],[copy(P.morts)],[copy(P.immunisés)] #On copie les données de la population dan des listes qui enregistreront les données de toute la simulation
    P.timer=[temps_guerison for i in range(P.n)] #on modifie le timer de guérison en fonction des données de la simulation
    for t in range(duree-1):
        P.propagation(pas,rayon_propagation,proba_infection,proba_mort) #On passe à l'instant d'après
        X+=[copy(P.x)] #On enregistre la position des individus et leur état
        Y+=[copy(P.y)]
        S+=[copy(P.sains)]
        I+=[copy(P.infectés)]
        R+=[copy(P.rétablis)]
        M+=[copy(P.morts)]
        N+=[copy(P.immunisés)]
        print(str(100*(t+1)/duree)+"%")
    return X,Y,S,I,R,M,N

def simulation_into_csv(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort):
    """Fait la simulation de la population P sur une certaine duree elon certaines données (ne renvoie pas les listes mais les enregidtre dans un fichier csv pour qu'elles soient utilisées plus tard)"""
    Xfile=open('x.csv','w')
    Yfile=open('y.csv','w')
    Sfile=open('s.csv','w')
    Ifile=open('i.csv','w')
    Rfile=open('r.csv','w')
    Mfile=open('m.csv','w')
    Nfile=open('n.csv','n')
    Xwriter=csv.writer(Xfile)
    Ywriter=csv.writer(Yfile)
    Swriter=csv.writer(Sfile)
    Iwriter=csv.writer(Ifile)
    Rwriter=csv.writer(Rfile)
    Mwriter=csv.writer(Mfile)
    Nwriter=csv.writer(Nfile)

    P.timer=[temps_guerison for i in range(P.n)]
    for t in range(duree):
        Xwriter.writerow(P.x)
        Ywriter.writerow(P.y)
        Swriter.writerow(P.sains)
        Iwriter.writerow(P.infectés)
        Rwriter.writerow(P.rétablis)
        Mwriter.writerow(P.morts)
        Nwriter.writerow(P.immunisés)
        P.propagation(pas,rayon_propagation,proba_infection,proba_mort)
        print(str(100*(t+1)/duree)+"%")

    Xfile.close()
    Yfile.close()
    Sfile.close()
    Ifile.close()
    Rfile.close()
    Mfile.close()
    Nfile.close()


def animation(P=population(0,0),frames=0,taille=0,frequence=1/60,pas=0.1,rayon_propagation=1,temps_guerison=-1,proba_infection=1,proba_mort=0,methode=simulation,Xfile='x.csv',Yfile='y.csv',Sfile='s.csv',Ifile='i.csv',Rfile='r.csv',Mfile='m.csv',Nfile='n.csv'):
    """Affiche une animation à partir d'une nouvelle simulation grâce aux arguments de la fonction, ou à partir de fichiers csv"""
    if methode==simulation:
        X,Y,S,I,R,M,N=methode(P,frames,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort)
        if taille==0: taille=P.r
    else:
        X,Y,S,I,R,M,N=methode(Xfile,Yfile,Sfile,Ifile,Rfile,Mfile,Nfile)
        if frames==0: frames=len(X)
        if taille==0: taille=max([max(x) for x in X])

    plt.suptitle("Évolution de l'épidémie dans le temps",fontsize=20)
    plt.subplots_adjust(left=0.05,right=0.95,bottom=0.08) #espacement entre les graphiques

    plt.subplot(1,2,1) #Graphique de gauche : animation du déplacement des individus en fonction du temps
    anim_sains,=plt.plot([],[],'.',color="green",label="Sains") #création des animations pour chaque état, idem que __repr__ (l.30-34)
    anim_infectés,=plt.plot([],[],'.',color="red",label="Infectés")
    anim_rétablis,=plt.plot([],[],'.',color="orange",label="Rétablis")
    anim_morts,=plt.plot([],[],'.',color="grey",label="Morts")
    anim_immunisés,=plt.plot([],[],'.',color="blue",label="Immunisés")

    plt.title('Animation')
    plt.xlim(0,taille) #On définit la taille maximale de l'espace
    plt.ylim(0,taille)
    plt.tick_params(axis='both',which='both',left=False,right=False,bottom=False,top=False,labelbottom=False,labelleft=False) #On modifie l'apparence du graphique (pas d'axe, ni de légende car ne sert à rien pour la position des points))

    plt.subplot(1,2,2) #Graphique de droite : animation de la courbe représentant le nombre d'individus dans chaque état en fonctiopn du temps
    graph_sains,=plt.plot([],[],color="green",label="Sains")
    graph_infectés,=plt.plot([],[],color="red",label="Infectés")
    graph_rétablis,=plt.plot([],[],color="orange",label="Rétablis")
    graph_morts,=plt.plot([],[],color="grey",label="Morts")

    plt.title('Graphique')
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend() #Affiche la légende
    plt.xlim(0,frames) #Fixe la limite du temps
    plt.ylim(0,len(X[0])) # Fixe le nombre maximal d'individus

    for f in range(frames): #Ajoute les données au graphique instant après instant
        anim_sains.set_xdata([X[f][i] for i in S[f]]) #Ajoute la position sur x des individus sains à l'animation correspondante
        anim_sains.set_ydata([Y[f][i] for i in S[f]]) #Ajoute la position sur y des individus sains à l'animation correspondante
        anim_infectés.set_xdata([X[f][i] for i in I[f]]) #Ajoute la position sur x des individus infectés à l'animation correspondante
        anim_infectés.set_ydata([Y[f][i] for i in I[f]]) #Ajoute la position sur y des individus infectés à l'animation correspondante
        anim_rétablis.set_xdata([X[f][i] for i in R[f]]) #Ajoute la position sur x des individus rétablis à l'animation correspondante
        anim_rétablis.set_ydata([Y[f][i] for i in R[f]]) #Ajoute la position sur y des individus rétablis à l'animation correspondante
        anim_morts.set_xdata([X[f][i] for i in M[f]]) #Ajoute la position sur x des individus morts à l'animation correspondante
        anim_morts.set_ydata([Y[f][i] for i in M[f]]) #Ajoute la position sur y des individus morts à l'animation correspondante
        anim_immunisés.set_xdata([X[f][i] for i in N[f]]) #Ajoute la position sur x des individus immunisés à l'animation correspondante
        anim_immunisés.set_ydata([Y[f][i] for i in N[f]]) #Ajoute la position sur y des individus immunisés à l'animation correspondante

        temps=[t for t in range(f)] #On crée la liste des tous les instants jusqu'à f de la simulation
        graph_sains.set_xdata(temps) #On met le temps en abscisse sur la courbe des sains
        graph_sains.set_ydata([len(S[t]) for t in temps]) #On met le nombre de sains à tous les instants inférieurs à f en ordonnée
        graph_infectés.set_xdata(temps) #On met le temps en abscisse sur la courbe des infectés
        graph_infectés.set_ydata([len(I[t]) for t in temps]) #On met le nombre d'infectés à tous les instants inférieurs à f en ordonnée
        graph_rétablis.set_xdata(temps) #On met le temps en abscisse sur la courbe des rétablis
        graph_rétablis.set_ydata([len(R[t]) for t in temps]) #On met le nombre de rétablis à tous les instants inférieurs à f en ordonnée
        graph_morts.set_xdata(temps) #On met le temps en abscisse sur la courbe des morts
        graph_morts.set_ydata([len(M[t]) for t in temps]) #On met le nombre de morts à tous les instants inférieurs à f en ordonnée

        plt.pause(frequence) #On attend la période fréquence entre deux images (ne fonctionne souvent pas car le temps de calcul graphique est supérieur à cette période)
        #plt.gcf().set_size_inches(21.5,10.8)
        #plt.savefig('sim frame'+str(f)+'.png')

        #On peut retirer les lignes du dessus des commentaires pour enregistrer chaque image de l'animation
    plt.show()

def graph(P=population(0,0),duree=0,pas=0.1,rayon_propagation=1,temps_guerison=-1,proba_infection=1,proba_mort=0,methode=simulation,Xfile='x.csv',Yfile='y.csv',Sfile='s.csv',Ifile='i.csv',Rfile='r.csv',Mfile='m.csv',Nfile='n.csv'):
    """Affiche la courbe des différents états des individus en fonction du temps"""
    #Le code est similaire à celui pour le graph de gauche de l'animation
    if methode==simulation:
        _,_,S,I,R,M,_=methode(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort)
    else:
        _,_,S,I,R,M,_=methode(Xfile,Yfile,Sfile,Ifile,Rfile,Mfile,Nfile)
        if duree==0: frames=len(S)

    temps=[t for t in range(duree)]
    plt.plot(temps,[len(S[t]) for t in temps],color="green",label="Sains")
    plt.plot(temps,[len(I[t]) for t in temps],color="red",label="Infectés")
    plt.plot(temps,[len(R[t]) for t in temps],color="orange",label="Rétablis")
    plt.plot(temps,[len(M[t]) for t in temps],color="grey",label="Morts")

    plt.ylim(0,P.n)

    plt.title("Évolution de l'épidémie dans le temps")
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()

    plt.show()

def sim_from_csv(Xfile,Yfile,Sfile,Ifile,Rfile,Mfile,Nfile):
    Xfile=open(Xfile)
    Yfile=open(Yfile)
    Sfile=open(Sfile)
    Ifile=open(Ifile)
    Rfile=open(Rfile)
    Mfile=open(Mfile)
    Nfile=open(Nfile)

    Xreader=csv.reader(Xfile)
    Yreader=csv.reader(Yfile)
    Sreader=csv.reader(Sfile)
    Ireader=csv.reader(Ifile)
    Rreader=csv.reader(Rfile)
    Mreader=csv.reader(Mfile)
    Nreader=csv.reader(Nfile)

    X,Y,S,I,R,M,N=[],[],[],[],[],[],[]
    for i in range(6): #Extrait chaque liste d'un csv une par une
        reader=[Xreader,Yreader,Sreader,Ireader,Rreader,Mreader][i]
        L=[X,Y,S,I,R,M][i]
        n_type=[float,float,int,int,int,int][i]
        for row in reader:
            L+=[[n_type(n) for n in row]]

    Xfile.close()
    Yfile.close()
    Sfile.close()
    Ifile.close()
    Rfile.close()
    Mfile.close()
    Nfile.close()

    return X,Y,S,I,R,M,N


P=population(500,30)
P.contaminer(5)
#P.immuniser(1)
#animation(methode=sim_from_csv)
animation(P,600,0,1/60,0.2,1,80,1/80,0.001)
#simulation_into_csv(P,200,0.2,1,50,1/2,0.001)
#input()
#graph(P,600,0.2,1,80,1/80,0.001)