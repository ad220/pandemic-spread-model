import random as rd
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import *

class population(object):
    def __init__(self,n=0,r=0):
        """Crée une population de n individus, de direction donnée, dans un espace carré de coté r"""
        pop=[[rd.randint(0,r) for i in range(n)],[rd.randint(0,r) for i in range(n)]] #Position de chaque point
        vx,vy=[],[] #Direction de chaque point selon x et y
        for _ in range(n):
            direction=rd.random()*2*pi #Direction aléatoire
            vx+=[cos(direction)] #direction selon x
            vy+=[sin(direction)] #direction selon y
        self.n = n #nombre d'individus
        self.r = r #taille de l'étude
        self.x = pop[0] #coordonnées sur x
        self.y = pop[1] #coordonnées sur y
        self.vx = vx #direction selon x
        self.vy = vy #direction selon y
        self.compteur = [0 for _ in range(n)]
        self.sains = [i for i in range(n)] #indices des individus sains
        self.exposés = [] #... contaminés mais pas contagieuses (et pas de symptômes)
        self.contagieux = [] #... contagieux mais pas encore de symptômes apparents
        self.infectés = [] #... infectés
        self.asymptomatiques = [] #... infectés mais sans symptômes
        self.isolés = [] #... infectés mais identifiés et isolés
        self.rétablis = [] #... rétablis
        self.morts = [] #... décédés
        self.confinés = [] #... confinés (repectent le confinement).

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
            i-=1

    def immuniser(self,n=0):
        """Immunise n éléments dans la population"""
        i=0
        for _ in range(n):
            while not i in self.sains:
                i+=1
            self.rétablis+=[i]
            self.sains.remove(i)
            i-=1

    def confiner(self,p):
        """Définit la partie de la population qui sera confinée et celle qui ne respectera pas le confinement"""
        pool=[-1] #Initialise la liste des éléments déjà confinés pour pas contaminer deux fois la même personne
        for i in range(p):
            random=-1 #un élément déjà dans pool pour entrer dans la boucle while
            while random in pool: #on vérifie que l'élément choisi n'a pas déjà été confiné
                random=rd.randint(0,self.n) #élément aléatoire
            pool+=[random]
            self.confinés+=[i] #contamination

    def propagation(self,pas,rayon_propagation,σ,Ɛ,γ,λ,α,μ,π,confinement): #Propage l'épidémie à l'instant suivant
        """Fait se déplacer chaque élément d'un déplacement m et vérifie si deux éléments sont susceptible de se contaminer leur distance relative < e"""
        b=self.r #on récupère la taille de l'espace
        X,Y,vX,vY=self.x,self.y,self.vx,self.vy #et les différentes caractéristiques de la population
        dS,dE,dC,dIso,dRi,dRa,dM=[],[],[],[],[],[],[]
        se_déplacent=self.sains+self.exposés+self.contagieux+self.infectés+self.asymptomatiques+self.rétablis
        if confinement : 
            for p in reversed(se_déplacent):
                if p in self.confinés: se_déplacent.remove(p)

        for p in se_déplacent: #On fait se déplacer tous les individus vivants non-confinés si confinement il y a selon leur direction d'une distance unitaire (pas) et vérifie que les éléments sont toujours dans l'espace d'étude sinon ils "rebondissent"
            X[p]+=pas*vX[p]
            Y[p]+=pas*vY[p]

            if X[p] > b :       X[p] , vX[p]  =  2*b-X[p] , -vX[p]
            elif X[p] < 0 :     X[p] , vX[p]  =  -X[p] , -vX[p]
            if Y[p] > b :       Y[p] , vY[p]  =  2*b-Y[p] , -vY[p]
            elif Y[p] < 0 :     Y[p] , vY[p]  =  -Y[p] , -vY[p]


        for p in self.exposés:
            self.compteur[p]+=1
            if self.compteur[p]>=Ɛ: dE+=[p]
        
        for p in self.contagieux:
            self.compteur[p]+=1
            if self.compteur[p]>=γ: dC+=[p]

        for p in self.infectés: #Si un élément sain et un autre infecté dont trop proches l'un de l'autre, ils ont une probabilité proba_infection de se contaminer
            self.compteur[p]+=1
            if rd.random()<μ: dM+=[p] #Chaque infecté a une probabilité μ proba_mort de mourrir à chaque instant
            elif self.compteur[p]>=λ: dRi+=[p] #Chaque infecté a une probabilité λ de guérir à chaque instant
            elif rd.random()<π: dIso+=[p]
            if p in se_déplacent:
                for s in self.sains:
                    if not s in dS and s in se_déplacent and rd.random()<σ and ((X[p]-X[s])**2 +(Y[p]-Y[s])**2)**(1/2)<rayon_propagation: dS+=[s]            
        
        for p in self.asymptomatiques:
            self.compteur[p]+=1
            if self.compteur[p]>=λ: dRa+=[p]

        for p in self.isolés:
            self.compteur[p]+=1
            if rd.random()<μ: dM+=[p] #Chaque infecté a une probabilité μ proba_mort de mourrir à chaque instant
            elif self.compteur[p]>=λ: dRi+=[p] #Chaque infecté a une probabilité λ de guérir à chaque instant


        for p in dS:
            self.exposés+=[p]
            self.sains.remove(p)

        for p in dE:
            self.contagieux+=[p]
            self.exposés.remove(p)

        for p in dC:
            if rd.random()<α: self.asymptomatiques+=[p]
            else: self.infectés+=[p]
            self.contagieux.remove(p)
        
        for p in dIso:
            self.isolés+=[p]
            self.infectés.remove(p)

        for p in dRi:
            self.rétablis+=[p]
            self.infectés.remove(p)

        for p in dRa:
            self.rétablis+=[p]
            self.asymptomatiques.remove(p)
        
        for p in dM:
            self.morts+=[p]
            self.infectés.remove(p)



def copy(objet): return [e for e in objet] #Copie d'une liste

def simulation(P,duree,pas,rayon_propagation,σ,Ɛ,γ,λ,α,μ,π,prop_inf_conf_deb,prop_inf_conf_fin):
    """Fait la simulation de la population P sur une certaine duree selon certaines données"""
    X,Y,S,E,C,I,A,R,M=[copy(P.x)],[copy(P.y)],[copy(P.sains)],[copy(P.exposés)],[copy(P.contagieux)],[copy(P.infectés)],[copy(P.asymptomatiques)],[copy(P.rétablis)],[copy(P.morts)] #On copie les données de la population dan des listes qui enregistreront les données de toute la simulation
    γ,λ=γ+Ɛ,λ+γ+Ɛ
    confinement=False
    for t in range(duree-1):
        n_infectés,n_vivants=len(P.infectés),P.n-len(P.morts)
        confinement=n_infectés > prop_inf_conf_deb*n_vivants or (n_infectés > prop_inf_conf_fin*n_vivants and confinement)
        P.propagation(pas,rayon_propagation,σ,Ɛ,γ,λ,α,μ,π,confinement) #On passe à l'instant d'après
        X+=[copy(P.x)] #On enregistre la position des individus et leur état
        Y+=[copy(P.y)]
        S+=[copy(P.sains)]
        E+=[copy(P.exposés)]
        C+=[copy(P.contagieux)]
        I+=[copy(P.infectés)]
        A+=[copy(P.asymptomatiques)]
        R+=[copy(P.rétablis)]
        M+=[copy(P.morts)]
        print(str(100*(t+1)/duree)+"%")
    return X,Y,S,E,C,I,A,R,M

def simulation_into_csv(P,duree,pas,rayon_propagation,σ,Ɛ,γ,λ,α,μ,π,prop_inf_conf_deb,prop_inf_conf_fin):
    """Fait la simulation de la population P sur une certaine duree selon certaines données (ne renvoie pas les listes mais les enregidtre dans un fichier csv pour qu'elles soient utilisées plus tard)"""
    
    fichiers=[open('x.csv','w'),open('y.csv','w'),open('s.csv','w'),open('e.csv','w'),open('c.csv','w'),open('i.csv','w'),open('a.csv','w'),open('r.csv','w'),open('m.csv','w')]
    écriveurs=[csv.writer(f) for f in fichiers]

    γ,λ=γ+Ɛ,λ+γ+Ɛ
    confinement=False
    for t in range(duree):
        L=[[round(x,2) for x in P.x],[round(y,2) for y in P.y],P.sains,P.exposés,P.contagieux,P.infectés,P.asymptomatiques,P.rétablis,P.morts]
        for i in range(9): écriveurs[i].writerow(L[i])
        n_infectés,n_vivants=len(P.infectés),P.n-len(P.morts)
        confinement=n_infectés > prop_inf_conf_deb*n_vivants or (n_infectés > prop_inf_conf_fin*n_vivants and confinement)
        P.propagation(pas,rayon_propagation,σ,Ɛ,γ,λ,α,μ,π,confinement)
        print(str(100*(t+1)/duree)+"%")
    for f in fichiers: f.close()

def sim_from_csv(Xfile,Yfile,Sfile,Efile,Cfile,Ifile,Afile,Rfile,Mfile):
    fichiers = [open(Xfile),open(Yfile),open(Sfile),open(Efile),open(Cfile),open(Ifile),open(Afile),open(Rfile),open(Mfile)]
    lecteurs = [csv.reader(f) for f in fichiers]

    X,Y,S,E,C,I,A,R,M=[],[],[],[],[],[],[],[],[]
    for i in range(9): #Extrait chaque liste d'un csv une par une
        reader=lecteurs[i]
        L=[X,Y,S,E,C,I,A,R,M][i]
        n_type=[float,float,int,int,int,int,int,int,int][i]
        for row in reader:
            L+=[[n_type(n) for n in row]]

    for f in fichiers: f.close()
    return X,Y,S,E,C,I,A,R,M

def anim(P=population(0,0),frames=0,taille=0,frequence=1/60,pas=0.1,rayon_propagation=1,σ=1,Ɛ=0,γ=0,λ=0,α=0,μ=0,π=0,prop_inf_conf_deb=1,prop_inf_conf_fin=1,methode=simulation,Xfile='x.csv',Yfile='y.csv',Sfile='s.csv',Efile='e.csv',Cfile='c.csv',Ifile='i.csv',Afile='a.csv',Rfile='r.csv',Mfile='m.csv'):
    """Affiche une animation à partir d'une nouvelle simulation grâce aux arguments de la fonction, ou à partir de fichiers csv"""
    
    
    
    #Pour isolés, on retire de l'anim mais on crée un autre graphique avec les isolés
    
    
    
    if methode==simulation:
        X,Y,S,E,C,I,A,R,M=methode(P,frames,pas,rayon_propagation,σ,Ɛ,γ,λ,α,μ,π,prop_inf_conf_deb,prop_inf_conf_fin)
        if taille==0: taille=P.r
    else:
        X,Y,S,E,C,I,A,R,M=methode(Xfile,Yfile,Sfile,Efile,Cfile,Ifile,Afile,Rfile,Mfile)
        if frames==0: frames=len(X)
        if taille==0: taille=max(X[0])

    fig,_=plt.subplots()
    fig.set_size_inches(21.6,10.8)
    plt.suptitle("Évolution de l'épidémie dans le temps",fontsize=20)
    plt.subplots_adjust(left=0.05,right=0.95,bottom=0.08) #espacement entre les graphiques

    plt.subplot(1,2,1) #Graphique de gauche : animation du déplacement des individus en fonction du temps
    anim_sains,=plt.plot([],[],'.',color="green",label="Sains") #création des animations pour chaque état, idem que __repr__ (l.30-34)
    anim_exposés,=plt.plot([],[],'.',color="#ff3636",label="Exposés")
    anim_contagieux,=plt.plot([],[],'.',color="#ff1414",label="Contagieux")
    anim_infectés,=plt.plot([],[],'.',color="#d40000",label="Infectés")
    anim_asymptomatiques,=plt.plot([],[],'.',color="orange",label="asymptomatiques")
    anim_rétablis,=plt.plot([],[],'.',color="blue",label="Rétablis")
    anim_morts,=plt.plot([],[],'.',color="#303030",label="Morts")

    plt.title('Animation')
    plt.xlim(0,taille) #On définit la taille maximale de l'espace
    plt.ylim(0,taille)
    plt.tick_params(axis='both',which='both',left=False,right=False,bottom=False,top=False,labelbottom=False,labelleft=False) #On modifie l'apparence du graphique (pas d'axe, ni de légende car ne sert à rien pour la position des points))

    plt.subplot(1,2,2) #Graphique de droite : animation de la courbe représentant le nombre d'individus dans chaque état en fonctiopn du temps
    graph_sains,=plt.plot([],[],color="green",label="Sains")
    graph_exposés,=plt.plot([],[],color="#ff3636",label="Exposés")
    graph_contagieux,=plt.plot([],[],color="#ff1414",label="Contagieux")
    graph_infectés,=plt.plot([],[],color="#d40000",label="Infectés")
    graph_asymptomatiques,=plt.plot([],[],color="orange",label="Asymptomatiques")
    graph_rétablis,=plt.plot([],[],color="blue",label="Rétablis")
    graph_morts,=plt.plot([],[],color="#303030",label="Morts")

    plt.title('Graphique')
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend() #Affiche la légende
    plt.xlim(0,frames) #Fixe la limite du temps
    plt.ylim(0,len(X[0])) # Fixe le nombre maximal d'individus

    def gen_frame(f):
        anim_sains.set_data([X[f][p] for p in S[f]],[Y[f][p] for p in S[f]]) #Ajoute la position des individus sains à l'animation correspondante
        anim_exposés.set_data([X[f][p] for p in E[f]],[Y[f][p] for p in E[f]]) #Ajoute la position des individus exposés à l'animation correspondante
        anim_contagieux.set_data([X[f][p] for p in C[f]],[Y[f][p] for p in C[f]]) #Ajoute la position des individus contagieux à l'animation correspondante
        anim_infectés.set_data([X[f][p] for p in I[f]],[Y[f][p] for p in I[f]]) #Ajoute la position des individus infectés à l'animation correspondante
        anim_asymptomatiques.set_data([X[f][p] for p in A[f]],[Y[f][p] for p in A[f]]) #Ajoute la position des individus asymptomatiques à l'animation correspondante
        anim_rétablis.set_data([X[f][p] for p in R[f]],[Y[f][p] for p in R[f]]) #Ajoute la position des individus rétablis à l'animation correspondante
        anim_morts.set_data([X[f][p] for p in M[f]],[Y[f][p] for p in M[f]]) #Ajoute la position des individus morts à l'animation correspondante

        temps=[t for t in range(f)] #On crée la liste des tous les instants jusqu'à f de la simulation
        graph_sains.set_data(temps,[len(S[t]) for t in temps]) #On met le nombre de sains à tous les instants inférieurs à f en ordonnée
        graph_exposés.set_data(temps,[len(E[t]) for t in temps]) #On met le nombre de sains à tous les instants inférieurs à f en ordonnée
        graph_contagieux.set_data(temps,[len(C[t]) for t in temps]) #On met le nombre de sains à tous les instants inférieurs à f en ordonnée
        graph_infectés.set_data(temps,[len(I[t]) for t in temps]) #On met le nombre d'infectés à tous les instants inférieurs à f en ordonnée
        graph_asymptomatiques.set_data(temps,[len(A[t]) for t in temps]) #On met le nombre de sains à tous les instants inférieurs à f en ordonnée
        graph_rétablis.set_data(temps,[len(R[t]) for t in temps]) #On met le nombre de rétablis à tous les instants inférieurs à f en ordonnée
        graph_morts.set_data(temps,[len(M[t]) for t in temps]) #On met le nombre de morts à tous les instants inférieurs à f en ordonnée
        return anim_sains,anim_exposés,anim_contagieux,anim_infectés,anim_asymptomatiques,anim_rétablis,anim_morts,graph_sains,graph_exposés,graph_contagieux,graph_infectés,graph_asymptomatiques,graph_rétablis,graph_morts
    
    ani=animation.FuncAnimation(fig=fig, func=gen_frame, frames=range(frames), interval=frequence*1000, blit=True)
    # ani.save('simvid.mp4',writer='ffmpeg')
    plt.show()

def graph(P=population(0,0),duree=0,pas=0.1,rayon_propagation=1,σ=1,Ɛ=0,γ=0,λ=0,α=0,μ=0,π=0,prop_inf_conf_deb=1,prop_inf_conf_fin=1,methode=simulation,Xfile='x.csv',Yfile='y.csv',Sfile='s.csv',Efile='e.csv',Cfile='c.csv',Ifile='i.csv',Afile='a.csv',Rfile='r.csv',Mfile='m.csv',Nfile='n.csv'):
    """Affiche la courbe des différents états des individus en fonction du temps"""
    #Le code est similaire à celui pour le graph de gauche de l'animation
    if methode==simulation:
        _,_,S,E,C,I,A,R,M=methode(P,duree,pas,rayon_propagation,σ,Ɛ,γ,λ,α,μ,π,prop_inf_conf_deb,prop_inf_conf_fin)
    else:
        _,_,S,E,C,I,A,R,M=methode(Xfile,Yfile,Sfile,Efile,Cfile,Ifile,Afile,Rfile,Mfile)
        if duree==0: duree=len(S)

    temps=[t for t in range(duree)]
    plt.plot(temps,[len(S[t]) for t in temps],color="green",label="Sains")
    plt.plot(temps,[len(E[t]) for t in temps],color="#ff3636",label="Exposés")
    plt.plot(temps,[len(C[t]) for t in temps],color="#ff1414",label="Contagieux")
    plt.plot(temps,[len(I[t]) for t in temps],color="#d40000",label="Infectés")
    plt.plot(temps,[len(A[t]) for t in temps],color="orange",label="Asymptomatiques")
    plt.plot(temps,[len(R[t]) for t in temps],color="blue",label="Rétablis")
    plt.plot(temps,[len(M[t]) for t in temps],color="#303030",label="Morts")

    plt.ylim(0,P.n)

    plt.title("Évolution de l'épidémie dans le temps")
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()

    plt.show()




# P=population(1000,25)
# P.contaminer(8)
# P.confiner(720)
# simulation_into_csv(P,1000,pas=0.3,rayon_propagation=1.2,σ=0.2,Ɛ=2*5,γ=4*5,λ=8*5,α=0.05,μ=0.005/5,π=0,prop_inf_conf_deb=0.05,prop_inf_conf_fin=0.02)
# anim(methode=sim_from_csv)
# graph(methode=sim_from_csv)

# P=population(10000,600)
# P.contaminer(10)
# P.confiner(9200)
# simulation_into_csv(P,2000,pas=0.3,rayon_propagation=1.2,σ=0.2,Ɛ=2*10,γ=4*10,λ=8*10,α=0.05,μ=0.005/10,π=0,prop_inf_conf_deb=0.01,prop_inf_conf_fin=0.001)

P=population(1500,140)
P.contaminer(3)
P.confiner(750)
graph(P,5000,0.25,1,1,24,40,144,0.2,0.001/8,0,0.025,0.012,methode=simulation)
# breakpoint()