import random as rd
import csv
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

    def propagation(self,pas,rayon_propagation,proba_infection,proba_mort):
        """Fait se déplacer chaque élément d'un déplacement m et vérifie si deux éléments sont susceptible de se contaminer leur distance relative < e"""
        b=self.r
        X,Y,vX,vY=self.x,self.y,self.vx,self.vy
        for i in range(self.n):
            if i in self.sains+self.infectés+self.rétablis:
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
    

    def reset(self):
        """réinitialise la population à partir de la liste init"""
        self.x=self.init[0]
        self.x=self.init[1]
        self.vx=self.init[2]
        self.vx=self.init[3]

def copy(objet): return [e for e in objet]

def simulation(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort):
    """fait la simulation de la population P sur une certaine duree"""
    X,Y,S,I,R,M=[copy(P.x)],[copy(P.y)],[copy(P.sains)],[copy(P.infectés)],[copy(P.rétablis)],[copy(P.morts)]
    P.timer=[temps_guerison for i in range(P.n)]
    for t in range(duree-1):
        P.propagation(pas,rayon_propagation,proba_infection,proba_mort) #fait chaque calcul de propagation
        X+=[copy(P.x)] #récupère la position de chaque point entre chaque déplacement
        Y+=[copy(P.y)]
        S+=[copy(P.sains)]
        I+=[copy(P.infectés)]
        R+=[copy(P.rétablis)]
        M+=[copy(P.morts)]
        print(str(100*(t+1)/duree)+"%")
    return X,Y,S,I,R,M

def simulation_into_csv_bourrin(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort,csvname,method):
    """fait la simulation de la population P sur une certaine duree"""
    sim_file=open(csvname,method)
    simW=csv.writer(sim_file, delimiter=';')

    P.timer=[temps_guerison for i in range(P.n)]
    for t in range(duree-1):
        simW.writerow((P.x,P.y,P.sains,P.infectés,P.rétablis,P.morts))
        P.propagation(pas,rayon_propagation,proba_infection,proba_mort)
        print(str(100*(t+1)/duree)+"%")

    sim_file.close()

def simulation_into_csv(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort):
    """fait la simulation de la population P sur une certaine duree"""
    X=open('x.csv','w')
    Y=open('y.csv','w')
    S=open('s.csv','w')
    I=open('i.csv','w')
    R=open('r.csv','w')
    M=open('m.csv','w')
    xWriter=csv.writer(X)
    yWriter=csv.writer(Y)
    sWriter=csv.writer(S)
    iWriter=csv.writer(I)
    rWriter=csv.writer(R)
    mWriter=csv.writer(M)

    P.timer=[temps_guerison for i in range(P.n)]
    for t in range(duree-1):
        xWriter.writerow(P.x)
        yWriter.writerow(P.y)
        sWriter.writerow(P.sains)
        iWriter.writerow(P.infectés)
        rWriter.writerow(P.rétablis)
        mWriter.writerow(P.morts)
        P.propagation(pas,rayon_propagation,proba_infection,proba_mort)
        print(str(100*(t+1)/duree)+"%")

    X.close()
    Y.close()
    S.close()
    I.close()
    R.close()
    M.close()


def animation(P,frames,frequence,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort): #changer proba_mort : recalculer en fonction de temps de duree étude
    plt.title("Évolution de l'épidémie dans le temps")

    plt.subplot(1,2,1)
    anim_sains,=plt.plot([],[],'.',color="green",label="Sains")
    anim_infectés,=plt.plot([],[],'.',color="red",label="Infectés")
    anim_rétablis,=plt.plot([],[],'.',color="orange",label="Rétablis")
    anim_morts,=plt.plot([],[],'.',color="grey",label="Morts")

    plt.xlim(0,P.r)
    plt.ylim(0,P.r)

    plt.subplot(1,2,2)
    graph_sains,=plt.plot([],[],color="green",label="Sains") #crée la figure
    graph_infectés,=plt.plot([],[],color="red",label="Infectés")
    graph_rétablis,=plt.plot([],[],color="orange",label="Rétablis")
    graph_morts,=plt.plot([],[],color="grey",label="Morts")
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()

    plt.xlim(0,frames)
    plt.ylim(0,P.n)

    X,Y,S,I,R,M=simulation(P,frames,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort)

    for f in range(frames):
        anim_sains.set_xdata([X[f][i] for i in S[f]])
        anim_sains.set_ydata([Y[f][i] for i in S[f]])
        anim_infectés.set_xdata([X[f][i] for i in I[f]])
        anim_infectés.set_ydata([Y[f][i] for i in I[f]])
        anim_rétablis.set_xdata([X[f][i] for i in R[f]])
        anim_rétablis.set_ydata([Y[f][i] for i in R[f]])
        anim_morts.set_xdata([X[f][i] for i in M[f]])
        anim_morts.set_ydata([Y[f][i] for i in M[f]])

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
        #plt.savefig('sim frame'+str(f)+'.png')
    plt.show()

def graph(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort):
    _,_,S,I,R,M=simulation(P,duree,pas,rayon_propagation,temps_guerison,proba_infection,proba_mort)
    
    temps=[t for t in range(duree)]
    plt.plot(temps,[len(S[t]) for t in temps],color="green",label="Sains") #crée la figure
    plt.plot(temps,[len(I[t]) for t in temps],color="red",label="Infectés")
    plt.plot(temps,[len(R[t]) for t in temps],color="orange",label="Rétablis")
    plt.plot(temps,[len(M[t]) for t in temps],color="grey",label="Morts")

    plt.ylim(0,P.n)

    plt.title("Évolution de l'épidémie dans le temps")
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()

    plt.show()

def graph_from_csv_bourrin(csvfile):
    simcsv=open(csvfile)
    simreader=csv.reader(simcsv, delimiter=';')
    S,I,R,M=[],[],[],[]
    for row in simreader:
        if row!=[]:
            _,_,s,i,r,m=row
            S+=[int(len(s)/3)]
            I+=[int(len(i)/3)]
            R+=[int(len(r)/3)]
            M+=[int(len(m)/3)]
    simcsv.close()

    duree=len(S)
    temps=[t for t in range(duree)]
    plt.plot(temps,[S[t] for t in temps],color="green",label="Sains") #crée la figure
    plt.plot(temps,[I[t] for t in temps],color="red",label="Infectés")
    plt.plot(temps,[R[t] for t in temps],color="orange",label="Rétablis")
    plt.plot(temps,[M[t] for t in temps],color="grey",label="Morts")

    plt.title("Évolution de l'épidémie dans le temps")
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()

    plt.savefig('test.png')
    
def graph_from_csv(Xfile,Yfile,Sfile,Ifile,Rfile,Mfile):
    Sfile=open(Sfile)
    Ifile=open(Ifile)
    Rfile=open(Rfile)
    Mfile=open(Mfile)

    Sreader=csv.reader(Sfile)
    Ireader=csv.reader(Ifile)
    Rreader=csv.reader(Rfile)
    Mreader=csv.reader(Mfile)

    S,I,R,M=[],[],[],[]
    for i in range(4):
        reader=[Sreader,Ireader,Rreader,Mreader][i]
        L=[S,I,R,M][i]
        for row in reader:
            L+=[len(row)]
    
    Sfile.close()
    Ifile.close()
    Rfile.close()
    Mfile.close()

    duree=len(S)
    temps=[t for t in range(duree)]
    plt.plot(temps,[S[t] for t in temps],color="green",label="Sains") #crée la figure
    plt.plot(temps,[I[t] for t in temps],color="red",label="Infectés")
    plt.plot(temps,[R[t] for t in temps],color="orange",label="Rétablis")
    plt.plot(temps,[M[t] for t in temps],color="grey",label="Morts")

    plt.title("Évolution de l'épidémie dans le temps")
    plt.xlabel('Temps (ua)')
    plt.ylabel('Nombre de personnes')
    plt.legend()

    plt.savefig('simulation.png')

#P=population(100,15)
#P.contaminer(2)
#animation(P,200,1/60,0.2,1,50,1/2,0.001)
#graph(P,600,0.15,1,150,1/3,0.001)
#simulation_into_csv(P,200,0.2,1,50,1/2,0.001)
#input()
graph_from_csv('x.csv','y.csv','s.csv','i.csv','r.csv','m.csv')
breakpoint()
