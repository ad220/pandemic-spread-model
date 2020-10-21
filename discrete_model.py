import random as rd
import csv
import matplotlib.pyplot as plt
from math import *

class population(object):
    def __init__(self,n=0,r=0):
        """Crée une population de n individus, de direction donnée, dans un espace carré de coté r"""
        pop=[[rd.random()*r for i in range(n)],[rd.random()*r for i in range(n)]] #Position de chaque point
        vx,vy=[],[]
        for i in range(n):
            direction=rd.random()*2*pi #Direction aléatoire
            vx+=[cos(direction)] #Direction selon x
            vy+=[sin(direction)] #Direction selon y
        self.n = n
        self.r = r
        self.x = pop[0]
        self.y = pop[1]
        self.vx = vx
        self.vy = vy
        self.timer = [-1 for i in range(n)]
        self.sains = [i for i in range(n)]
        self.infectés = []
        self.rétablis = []
        self.morts = []
        self.immunisés = []
        self.isolés =[]

    def __repr__(self):
        return "Population de "+str(P.n)+" individus, dans un espace carré de côté "+str(P.r)+" (ua), dont "+str(len(self.sains))+" personnes saines, "+str(len(self.infectés))+" infectées, "+str(len(self.rétablis))+" rétablies, et "+str(len(self.morts))+" mortes."

    def contaminer(self,n=1):
        """Contamine n éléments dans la population"""
        i=0
        for _ in range(n):
            while not i in self.sains:
                i+=1
            self.infectés+=[i]
            self.sains.remove(i)
    
    def immuniser(self,n=0):
        """Immunise n éléments dans la population"""
        i=0
        for _ in range(n):
            while not i in self.sains:
                i+=1
            self.immunisés+=[i]
            self.sains.remove(i)

    def propagation(self,pas,rayon_propagation,proba_infection,proba_mort):
        """Fait se déplacer chaque élément d'un déplacement m et vérifie si deux éléments sont susceptible de se contaminer leur distance relative < e"""
        b=self.r
        X,Y,vX,vY=self.x,self.y,self.vx,self.vy
        for i in range(self.n):
            if i in self.sains+self.infectés+self.rétablis+self.immunisés:
                X[i]+=pas*vX[i]
                Y[i]+=pas*vY[i]

        for i in range(self.n): #On vérifie que les éléments sont toujours dans l'espace d'étude sinon ils "rebondissent"
            if X[i] > b :       X[i] , vX[i]  =  b , -vX[i]
            elif X[i] < 0 :     X[i] , vX[i]  =  0 , -vX[i]
            if Y[i] > b :       Y[i] , vY[i]  =  b , -vY[i]
            elif Y[i] < 0 :     Y[i] , vY[i]  =  0 , -vY[i]

        for i in self.infectés: #on vérifie si les éléments sont trop proches deux à deux (complexité en n!)
            for j in self.sains:
                if rd.random()<proba_infection and ((X[i]-X[j])**2 +(Y[i]-Y[j])**2)**(1/2)<rayon_propagation:
                        self.infectés+=[j]
                        self.sains.remove(j)

        for i in self.infectés:
            if self.timer[i]==0:
                self.rétablis+=[i]
                self.infectés.remove(i)
            elif rd.random()<proba_mort:
                self.infectés.remove(i)
                self.morts+=[i]
            self.timer[i]-=1

        self.x,self.y=X,Y


def copy(objet): return [e for e in objet]

def simulation(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort):
    """fait la simulation de la population P sur une certaine duree"""
    X,Y,S,I,R,M,N=[copy(P.x)],[copy(P.y)],[copy(P.sains)],[copy(P.infectés)],[copy(P.rétablis)],[copy(P.morts)],[copy(P.immunisés)]
    P.timer=[temps_guerison for i in range(P.n)]
    for t in range(duree-1):
        P.propagation(pas,rayon_propagation,proba_infection,proba_mort)
        X+=[copy(P.x)]
        Y+=[copy(P.y)]
        S+=[copy(P.sains)]
        I+=[copy(P.infectés)]
        R+=[copy(P.rétablis)]
        M+=[copy(P.morts)]
        N+=[copy(P.immunisés)]
        print(str(100*(t+1)/duree)+"%")
    return X,Y,S,I,R,M,N

def simulation_into_csv(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort):
    """Fait la simulation de la population P sur une certaine duree"""
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
    if methode==simulation: 
        X,Y,S,I,R,M,N=methode(P,frames,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort)
        if taille==0: taille=P.r
    else: 
        X,Y,S,I,R,M,N=methode(Xfile,Yfile,Sfile,Ifile,Rfile,Mfile,Nfile)
        if frames==0: frames=len(X)
        if taille==0: taille=max([max(x) for x in X])
        
    plt.suptitle("Évolution de l'épidémie dans le temps",fontsize=20)
    plt.subplots_adjust(left=0.05,right=0.95,bottom=0.08)
    
    
    plt.subplot(1,2,1)
    anim_sains,=plt.plot([],[],'.',color="green",label="Sains")
    anim_infectés,=plt.plot([],[],'.',color="red",label="Infectés")
    anim_rétablis,=plt.plot([],[],'.',color="orange",label="Rétablis")
    anim_morts,=plt.plot([],[],'.',color="grey",label="Morts")
    anim_immunisés,=plt.plot([],[],'.',color="blue",label="Immunisés")

    plt.title('Animation')
    plt.xlim(0,taille)
    plt.ylim(0,taille)
    plt.tick_params(axis='both',which='both',left=False,right=False,bottom=False,top=False,labelbottom=False,labelleft=False)

    plt.subplot(1,2,2)
    graph_sains,=plt.plot([],[],color="green",label="Sains") #crée la figure
    graph_infectés,=plt.plot([],[],color="red",label="Infectés")
    graph_rétablis,=plt.plot([],[],color="orange",label="Rétablis")
    graph_morts,=plt.plot([],[],color="grey",label="Morts")
    
    plt.title('Graphique')
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()
    plt.xlim(0,frames)
    plt.ylim(0,len(X[0]))

    for f in range(frames):
        anim_sains.set_xdata([X[f][i] for i in S[f]])
        anim_sains.set_ydata([Y[f][i] for i in S[f]])
        anim_infectés.set_xdata([X[f][i] for i in I[f]])
        anim_infectés.set_ydata([Y[f][i] for i in I[f]])
        anim_rétablis.set_xdata([X[f][i] for i in R[f]])
        anim_rétablis.set_ydata([Y[f][i] for i in R[f]])
        anim_morts.set_xdata([X[f][i] for i in M[f]])
        anim_morts.set_ydata([Y[f][i] for i in M[f]])
        anim_immunisés.set_xdata([X[f][i] for i in N[f]])
        anim_immunisés.set_ydata([Y[f][i] for i in N[f]])

        temps=[t for t in range(f)]
        graph_sains.set_xdata(temps)
        graph_sains.set_ydata([len(S[t]) for t in temps])
        graph_infectés.set_xdata(temps)
        graph_infectés.set_ydata([len(I[t]) for t in temps])
        graph_rétablis.set_xdata(temps)
        graph_rétablis.set_ydata([len(R[t]) for t in temps])
        graph_morts.set_xdata(temps)
        graph_morts.set_ydata([len(M[t]) for t in temps])

        plt.pause(frequence)
        #plt.gcf().set_size_inches(21.5,10.8)
        #plt.savefig('sim frame'+str(f)+'.png')
    plt.show()

def graph(P=population(0,0),duree=0,pas=0.1,rayon_propagation=1,temps_guerison=-1,proba_infection=1,proba_mort=0,methode=simulation,Xfile='x.csv',Yfile='y.csv',Sfile='s.csv',Ifile='i.csv',Rfile='r.csv',Mfile='m.csv',Nfile='n.csv'):
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
    for i in range(6):
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
    

P=population(600,30)
P.contaminer(5)
P.immuniser(0)
print(P)
#animation(methode=sim_from_csv)
#animation(P,600,0,1/60,0.2,1,80,1/80,0.002)
#simulation_into_csv(P,200,0.2,1,50,1/2,0.001)
#input()
graph(P,800,0.2,1,120,1/120,0.001)