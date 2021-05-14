#Pas encore commenté !!!

from multiprocessing import Pool
import random as rd
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import pi,cos,sin

def infectar(simExt):
    p,c,S,seDéplacent,X,Y,μ,λ,χ,σ,r=simExt
    c+=1
    dMi,dRi,dQ,dS=[]*4
    if rd.random()<μ: dMi=[p] #Chaque infecté a une probabilité μ proba_mort de mourrir à chaque instant
    elif c>=λ: dRi=[p] #Chaque infecté a une probabilité λ de guérir à chaque instant
    elif rd.random()<χ: dQ=[p]
    if p in seDéplacent:
        for s in S:
            if not s in dS and s in seDéplacent and rd.random()<σ and ((X[p]-X[s])**2 +(Y[p]-Y[s])**2)**(1/2)<r: dS=[s] 
    return dMi,dRi,dQ,dS


class population(object):
    def __init__(self,n=0,r=0):
        """Crée une population de n individus, de direction donnée, dans un espace carré de coté r"""
        pop=[[rd.random()*r for i in range(n)],[rd.random()*r for i in range(n)]] #Position de chaque point
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
        self.enQuarantaine = [] #... infectés mais identifiés et isolés
        self.rétablis = [] #... rétablis
        self.morts = [] #... décédés
        self.confinés = [] #... confinés (repectent le confinement).

    def infecter(self,n=1): #Contamine les n premiers éléments sains de la population (reste aléatoire car leur position l'est)
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

    def propagation(self,pas,r,σ,Ɛ,γ,λ,α,μ,χ,confinement,nT): #Propage l'épidémie à l'instant suivant
        """Fait se déplacer chaque élément d'un déplacement m et vérifie si deux éléments sont susceptible de se contaminer leur distance relative < e"""
        b=self.r #on récupère la taille de l'espace
        X,Y,vX,vY=self.x,self.y,self.vx,self.vy #et les différentes caractéristiques de la population
        dS,dE,dC,dQ,dRi,dRq,dRa,dMi,dMq=[],[],[],[],[],[],[],[],[]
        seDéplacent=self.sains+self.exposés+self.contagieux+self.infectés+self.asymptomatiques+self.rétablis
        if confinement : 
            for p in reversed(seDéplacent):
                if p in self.confinés: seDéplacent.remove(p)

        for p in seDéplacent: #On fait se déplacer tous les individus vivants non-confinés si confinement il y a selon leur direction d'une distance unitaire (pas) et vérifie que les éléments sont toujours dans l'espace d'étude sinon ils "rebondissent"
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

        # p,C,S,seDéplacent,X,Y,μ,λ,χ,σ,r=simExt


        p=Pool(nT)
        L=[(self.infectés[p],self.compteur[p],self.sains,seDéplacent,X,Y,μ,λ,χ,σ,r) for p in range(len(self.infectés))]
        D=p.map(infectar,L)
        dMi+=[D[p][0] for p in range(len(self.infectés))]
        dRi+=[D[p][1] for p in range(len(self.infectés))]
        dQ+=[D[p][2] for p in range(len(self.infectés))]
        dS+=[D[p][3] for p in range(len(self.infectés))]


        for p in self.enQuarantaine:
            self.compteur[p]+=1
            if rd.random()<μ: dMq+=[p] #Chaque infecté a une probabilité μ proba_mort de mourrir à chaque instant
            elif self.compteur[p]>=λ: dRq+=[p] #Chaque infecté a une probabilité λ de guérir à chaque instant

        for p in self.asymptomatiques:
            self.compteur[p]+=1
            if self.compteur[p]>=λ: dRa+=[p]



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
        
        for p in dQ:
            self.enQuarantaine+=[p]
            self.infectés.remove(p)

        for p in dRi:
            self.rétablis+=[p]
            self.infectés.remove(p)

        for p in dRq:
            self.rétablis+=[p]
            self.enQuarantaine.remove(p)

        for p in dRa:
            self.rétablis+=[p]
            self.asymptomatiques.remove(p)
        
        for p in dMi:
            self.morts+=[p]
            self.infectés.remove(p)

        for p in dMq:
            self.morts+=[p]
            self.enQuarantaine.remove(p)



    def infection(self,μ,χ,σ,λ,thread,nT,seDéplacent,r):
        I=self.infectés
        dMi,dRi,dQ,dS=[],[],[],[]
        for p in I[thread*len(len(I)/nT):(thread+1)*len(len(I)/nT)]:
            self.compteur[p]+=1
            if rd.random()<μ: dMi+=[p] #Chaque infecté a une probabilité μ proba_mort de mourrir à chaque instant
            elif self.compteur[p]>=λ: dRi+=[p] #Chaque infecté a une probabilité λ de guérir à chaque instant
            elif rd.random()<χ: dQ+=[p]
            if p in seDéplacent:
                for s in self.sains:
                    if not s in dS and s in seDéplacent and rd.random()<σ and ((self.x[p]-self.x[s])**2 +(self.y[p]-self.y[s])**2)**(1/2)<r: dS+=[s]
        return dMi,dRi,dQ,dS
        



def copy(objet): return [e for e in objet] #Copie d'une liste

def simulation(P,duree,dt,pas,r,σ,Ɛ,γ,λ,α=0,μ=0,χ=0,PICD=1,PICF=1,nT=1):
    """Fait la simulation de la population P sur une certaine duree selon certaines données"""
    X,Y,S,E,C,I,Q,A,R,M=[copy(P.x)],[copy(P.y)],[copy(P.sains)],[copy(P.exposés)],[copy(P.contagieux)],[copy(P.infectés)],[copy(P.enQuarantaine)],[copy(P.asymptomatiques)],[copy(P.rétablis)],[copy(P.morts)] #On copie les données de la population dan des listes qui enregistreront les données de toute la simulation
    γ,λ=γ+Ɛ,λ+γ+Ɛ
    confinement=False
    for t in range(duree-1):
        nInfectés,nVivants=len(P.infectés),P.n-len(P.morts)
        confinement=nInfectés > PICD*nVivants or (nInfectés > PICF*nVivants and confinement)
        P.propagation(pas,r,σ,Ɛ,γ,λ,α,μ,χ,confinement,nT) #On passe à l'instant d'après
        X+=[copy(P.x)] #On enregistre la position des individus et leur état
        Y+=[copy(P.y)]
        S+=[copy(P.sains)]
        E+=[copy(P.exposés)]
        C+=[copy(P.contagieux)]
        I+=[copy(P.infectés)]
        Q+=[copy(P.enQuarantaine)]
        A+=[copy(P.asymptomatiques)]
        R+=[copy(P.rétablis)]
        M+=[copy(P.morts)]
        print(str(100*(t+1)/duree)+"%")
    return X,Y,S,E,C,I,Q,A,R,M

def simulation_into_csv(P,duree,pas,r,σ,Ɛ,γ,λ,α=0,μ=0,χ=0,SDC=1,SFC=1,Xfile='x.csv',Yfile='y.csv',Sfile='s.csv',Efile='e.csv',Cfile='c.csv',Ifile='i.csv',Qfile='q.csv',Afile='a.csv',Rfile='r.csv',Mfile='m.csv'):
    """Fait la simulation de la population P sur une certaine duree selon certaines données (ne renvoie pas les listes mais les enregidtre dans un fichier csv pour qu'elles soient utilisées plus tard)"""
    fichiers=[open(Xfile,'w',newline=""),open(Yfile,'w',newline=""),open(Sfile,'w',newline=""),open(Efile,'w',newline=""),open(Cfile,'w',newline=""),open(Ifile,'w',newline=""),open(Qfile,'w',newline=""),open(Afile,'w',newline=""),open(Rfile,'w',newline=""),open(Mfile,'w',newline="")]
    écriveurs=[csv.writer(f) for f in fichiers]

    γ,λ=γ+Ɛ,λ+γ+Ɛ
    confinement=False
    for t in range(duree):
        L=[[round(x,2) for x in P.x],[round(y,2) for y in P.y],P.sains,P.exposés,P.contagieux,P.infectés,P.enQuarantaine,P.asymptomatiques,P.rétablis,P.morts]
        for i in range(10): écriveurs[i].writerow(L[i])
        nInfectés,nVivants=len(P.infectés+P.enQuarantaine),P.n-len(P.morts)
        confinement=nInfectés > SDC*nVivants or (nInfectés > SFC*nVivants and confinement)
        P.propagation(pas,r,σ,Ɛ,γ,λ,α,μ,χ,confinement)
        print(str(100*(t+1)/duree)+"%")
    for f in fichiers: f.close()

def multiSimIntoCsv(indiceDébut,indiceFin,n,dim,infectés,confinés,duree,pas,r,σ,Ɛ,γ,λ,α=0,μ=0,χ=0,SDC=1,SFC=1):
    for indice in range(indiceDébut,indiceFin):
        P=population(n,dim)
        P.infecter(infectés)
        P.confiner(confinés)
        simulation_into_csv(P,duree,pas,r,σ,Ɛ,γ,λ,α,μ,χ,SDC,SFC,'x'+str(indice)+'.csv','y'+str(indice)+'.csv','s'+str(indice)+'.csv','e'+str(indice)+'.csv','c'+str(indice)+'.csv','i'+str(indice)+'.csv','q'+str(indice)+'.csv','a'+str(indice)+'.csv','r'+str(indice)+'.csv','m'+str(indice)+'.csv')

def sim_from_csv(Xfile='x.csv',Yfile='y.csv',Sfile='s.csv',Efile='e.csv',Cfile='c.csv',Ifile='i.csv',Qfile='q.csv',Afile='a.csv',Rfile='r.csv',Mfile='m.csv'):
    fichiers = [open(Xfile),open(Yfile),open(Sfile),open(Efile),open(Cfile),open(Ifile),open(Qfile),open(Afile),open(Rfile),open(Mfile)]
    lecteurs = [csv.reader(f) for f in fichiers]

    X,Y,S,E,C,I,Q,A,R,M=[],[],[],[],[],[],[],[],[],[]
    for i in range(10): #Extrait chaque liste d'un csv une par une
        reader=lecteurs[i]
        L=[X,Y,S,E,C,I,Q,A,R,M][i]
        n_type=[float,float,int,int,int,int,int,int,int,int][i]
        for row in reader:
            L+=[[n_type(n) for n in row]]

    for f in fichiers: f.close()
    return X,Y,S,E,C,I,Q,A,R,M

def plotMultiSimFromCsv(indiceDébut,indiceFin):
    moyenneSimulations=[]
    _,_,S,E,C,I,Q,A,R,M=sim_from_csv('x'+str(indiceDébut)+'.csv','y'+str(indiceDébut)+'.csv','s'+str(indiceDébut)+'.csv','e'+str(indiceDébut)+'.csv','c'+str(indiceDébut)+'.csv','i'+str(indiceDébut)+'.csv','q'+str(indiceDébut)+'.csv','a'+str(indiceDébut)+'.csv','r'+str(indiceDébut)+'.csv','m'+str(indiceDébut)+'.csv')
    moyenneSimulations+=[[len(L) for L in S],[len(L) for L in E],[len(L) for L in C],[len(L) for L in I],[len(L) for L in Q],[len(L) for L in A],[len(L) for L in R],[len(L) for L in M]]
    duree=len(moyenneSimulations[0])
    temps=[t for t in range(duree)]
    N=indiceFin-indiceDébut
    for indice in range(indiceDébut+1,indiceFin):
        _,_,S,E,C,I,Q,A,R,M=sim_from_csv('x'+str(indice)+'.csv','y'+str(indice)+'.csv','s'+str(indice)+'.csv','e'+str(indice)+'.csv','c'+str(indice)+'.csv','i'+str(indice)+'.csv','q'+str(indice)+'.csv','a'+str(indice)+'.csv','r'+str(indice)+'.csv','m'+str(indice)+'.csv')
        simulation=[[len(L) for L in S],[len(L) for L in E],[len(L) for L in C],[len(L) for L in I],[len(L) for L in Q],[len(L) for L in A],[len(L) for L in R],[len(L) for L in M]]
        for categorie in moyenneSimulations:
            for t in temps:
                categorie[t]+=simulation[t]
        print(str(100*indice/N)+'%')
    for categorie in moyenneSimulations:
        for t in temps:
            categorie[t]/=N
    S,E,C,I,Q,A,R,M=moyenneSimulations

    totalInfectés=[I[t]+Q[t] for t in temps]
    plt.plot(temps,S,color="green",label="Sains")
    plt.plot(temps,E,color="orange",label="Exposés")
    plt.plot(temps,C,color="#ff7b00",label="Contagieux")
    plt.plot(temps,totalInfectés,color="purple",label="Total infectés")
    plt.plot(temps,I,'--',color="purple",label="Infectés")
    plt.plot(temps,A,color="red",label="Asymptomatiques")
    plt.plot(temps,R,color="blue",label="Rétablis")
    plt.plot(temps,M,color="black",label="Morts")

    plt.title("Évolution de l'épidémie dans le temps")
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()
    plt.show()



def anim(simulation,taille=0,frequence=1/60):
    """Affiche une animation à partir d'une nouvelle simulation grâce aux arguments de la fonction, ou à partir de fichiers csv"""
    
    
    
    #Pour isolés, on retire de l'anim mais on crée un autre graphique avec les isolés
    
    X,Y,S,E,C,I,Q,A,R,M=simulation
    duree=len(X)
    tI=[I[t]+Q[t] for t in range(duree)]
    if taille==0: taille=max([max(X[0]),max(Y[0])])

    fig,_=plt.subplots()
    fig.set_size_inches(21.6,10.8)
    plt.suptitle("Évolution de l'épidémie dans le temps",fontsize=20)
    plt.subplots_adjust(left=0.05,right=0.95,bottom=0.08) #espacement entre les graphiques

    plt.subplot(1,2,1) #Graphique de gauche : animation du déplacement des individus en fonction du temps
    anim_sains,=plt.plot([],[],'.',color="green",label="Sains") #création des animations pour chaque état, idem que __repr__ (l.30-34)
    anim_exposés,=plt.plot([],[],'.',color="orange",label="Exposés")
    anim_contagieux,=plt.plot([],[],'.',color="#ff7b00",label="Contagieux")
    anim_infectés,=plt.plot([],[],'.',color="purple",label="Infectés")
    anim_asymptomatiques,=plt.plot([],[],'.',color="red",label="Asymptomatiques")
    anim_rétablis,=plt.plot([],[],'.',color="blue",label="Rétablis")
    anim_morts,=plt.plot([],[],'.',color="#303030",label="Morts")

    plt.title('Animation')
    plt.xlim(0,taille) #On définit la taille maximale de l'espace
    plt.ylim(0,taille)
    plt.tick_params(axis='both',which='both',left=False,right=False,bottom=False,top=False,labelbottom=False,labelleft=False) #On modifie l'apparence du graphique (pas d'axe, ni de légende car ne sert à rien pour la position des points))

    plt.subplot(1,2,2) #Graphique de droite : animation de la courbe représentant le nombre d'individus dans chaque état en fonctiopn du temps
    graph_sains,=plt.plot([],[],color="green",label="Sains")
    graph_exposés,=plt.plot([],[],color="orange",label="Exposés")
    graph_contagieux,=plt.plot([],[],color="#ff7b00",label="Contagieux")
    graph_tInfectés,=plt.plot([],[],color="purple",label="Total infectés")
    graph_infectés,=plt.plot([],[],'--',color="purple",label="Infectés")
    graph_asymptomatiques,=plt.plot([],[],color="red",label="Asymptomatiques")
    graph_rétablis,=plt.plot([],[],color="blue",label="Rétablis")
    graph_morts,=plt.plot([],[],color="#303030",label="Morts")

    plt.title('Graphique')
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend() #Affiche la légende
    plt.xlim(0,duree) #Fixe la limite du temps
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
        graph_tInfectés.set_data(temps,[len(tI[t]) for t in temps])
        graph_infectés.set_data(temps,[len(I[t]) for t in temps]) #On met le nombre d'infectés à tous les instants inférieurs à f en ordonnée
        graph_asymptomatiques.set_data(temps,[len(A[t]) for t in temps]) #On met le nombre de sains à tous les instants inférieurs à f en ordonnée
        graph_rétablis.set_data(temps,[len(R[t]) for t in temps]) #On met le nombre de rétablis à tous les instants inférieurs à f en ordonnée
        graph_morts.set_data(temps,[len(M[t]) for t in temps]) #On met le nombre de morts à tous les instants inférieurs à f en ordonnée
        return anim_sains,anim_exposés,anim_contagieux,anim_infectés,anim_asymptomatiques,anim_rétablis,anim_morts,graph_sains,graph_exposés,graph_contagieux,graph_infectés,graph_asymptomatiques,graph_rétablis,graph_morts
    
    ani=animation.FuncAnimation(fig=fig, func=gen_frame, frames=range(duree), interval=frequence*1000, blit=True)
    # ani.save('simvid.mp4',writer='ffmpeg')
    plt.show()

def graph(simulation):
    """Affiche la courbe des différents états des individus en fonction du temps"""
    #Le code est similaire à celui pour le graph de gauche de l'animation
    _,_,S,E,C,I,Q,A,R,M=simulation
    duree=len(S)
    tI=[I[t]+Q[t] for t in range(duree)]

    temps=[t for t in range(duree)]
    plt.plot(temps,[len(S[t]) for t in temps],color="green",label="Sains")
    plt.plot(temps,[len(E[t]) for t in temps],color="orange",label="Exposés")
    plt.plot(temps,[len(C[t]) for t in temps],color="#ff7b00",label="Contagieux")
    plt.plot(temps,[len(tI[t]) for t in temps],color="purple",label="Total infectés")
    plt.plot(temps,[len(I[t]) for t in temps],'--',color="purple",label="Infectés")
    plt.plot(temps,[len(A[t]) for t in temps],color="red",label="Asymptomatiques")
    plt.plot(temps,[len(R[t]) for t in temps],color="blue",label="Rétablis")
    plt.plot(temps,[len(M[t]) for t in temps],color="#303030",label="Morts")
    S,E,C,I,Q,A,R,M=[],[],[],[],[],[],[],[]
    # plt.ylim(0,sum([len(simulation[i][0]) for i in range(2,10)]))

    plt.title("Évolution de l'épidémie dans le temps")
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()

    plt.show()

def densité(n,c,r): return c**2/(pi*r**2*n)


if __name__ == '__main__':

    # multiSimIntoCsv(0,2,100,31,2,60,200,0.4,1,1,3,5,14,0.4,0.005,1/22,0.25,0.12)
    # S=plotMultiSimFromCsv(0,500)
    # graph(S)

    # anim(P,frames=500,taille=0,frequence=1/60,pas=0.2,r=1,σ=1,Ɛ=3,γ=5,λ=24,α=0.2,μ=0.001,χ=0,PICD=0.08,PICF=0.03,methode=simulation)
    # S=sim_from_csv()
    # graph(S)

    # P=population(10000,600)
    # P.contaminer(10)
    # P.confiner(9200)
    # simulation_into_csv(P,2000,pas=0.3,r=1.2,σ=0.2,Ɛ=2*10,γ=4*10,λ=8*10,α=0.05,μ=0.005/10,χ=0,PICD=0.01,PICF=0.001)

    P=population(10000,60)
    P.infecter(10)
    P.confiner(650)
    S=simulation(P,400,pas=0.3,r=1.2,σ=0.2,Ɛ=2*10,γ=4*10,λ=8*10,α=0.05,μ=0.005/10,χ=0,PICD=0.01,PICF=0.001,nT=16)
    anim(S)

    #P=population(32,8)
    #P.contaminer(32)
    #animation(P,200,0,1/60,0.2,1,12,1/2,0.001,methode=simulation)
    # breakpoint()