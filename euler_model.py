"""Modèle Mathématique"""

import matplotlib.pyplot as plt

class population(object):
    def __init__(self,n=100,infectés=1,immunisés=0):
        """Crée une population de n individus"""
        self.n = n #Nombre d'individus...
        self.sains = n-immunisés-infectés #... sains
        self.exposés = 0 #... contaminés mais pas contagieux (et sans symptômes)
        self.contagieux = 0 #... contagieux mais pas encore de symptômes apparents
        self.infectés = infectés #... infectés
        self.asymptomatiques = 0 #... infectés mais sans symptôme
        self.enQuarantaine = 0 #infectés mais indentifié et isolé
        self.rétablis = immunisés #... rétablis ou déjà immunisés sans y avoir été exposés
        self.morts = 0 #... décédés


    def propagation_SIR(self,β,γ):
        """Propage le virus à l'instant selon le modèle SIR"""
        dS=int(self.sains*β*self.infectés)
        dI=int(self.infectés*γ)
        self.sains += -dS
        self.infectés += dS-dI
        self.rétablis += dI


    def propagation_SEIR(self,σ,Ɛ,λ,μ):
        """Propage le virus à l'instant selon le modèle SEIR"""
        n=self.n
        dS=σ/n*self.sains*self.infectés
        dE=Ɛ*self.exposés
        dR=λ*self.infectés
        dM=μ*self.infectés
        self.sains += -dS
        self.exposés += dS-dE
        self.infectés += dE-dR-dM
        self.rétablis += dR
        self.morts += dM


    def propagation_complete(self,dt,σ,Ɛ,γ,λ,α,μ,χ=0):
        """Propage le virus à l'instant selon le modèle complet"""
        n=self.n
        dS=σ/n*self.sains*(self.infectés+self.contagieux+self.asymptomatiques)*dt
        dE=Ɛ*self.exposés*dt
        dC=γ*self.contagieux*dt
        dQ=χ*self.infectés*dt
        dRi=λ*self.infectés*dt
        dRq=λ*self.enQuarantaine*dt
        dRa=λ*self.asymptomatiques*dt
        dMi=μ*self.infectés*dt
        dMq=μ*self.enQuarantaine*dt
        self.sains += -dS
        self.exposés += dS-dE
        self.contagieux += dE-dC
        self.infectés += (1-α)*dC-dRi-dMi-dQ
        self.asymptomatiques += α*dC-dRa
        self.enQuarantaine += dQ-dRq-dMq
        self.rétablis += dRi+dRa+dRq
        self.morts += dMi+dMq




"""Simulations"""
def simulation_SIR(P,duree,dt,β,γ):
    """Fait la simulation de l'épidémie avec P selon le modèle SIR"""
    S,I,R=[P.sains],[P.infectés],[P.rétablis]
    for _ in range(int(duree/dt)-1):
        P.propagation_SIR(β,γ)
        S+=[P.sains]
        I+=[P.infectés]
        R+=[P.rétablis]
    return [S,I,R]


def simulation_SEIR(P,duree,dt,σ,Ɛ,λ,μ):
    """Fait la simulation de l'épidémie avec P selon avec le modèle SEIR"""
    S,E,I,R=[P.sains],[P.exposés],[P.infectés],[P.rétablis]
    for _ in range(int(duree/dt)-1):
        P.propagation_SEIR(σ,Ɛ,λ,μ)
        S+=[P.sains]
        E+=[P.exposés]
        I+=[P.infectés]
        R+=[P.rétablis]
    return [S,E,I,R]


def simulation_complete(P,duree,dt,σ,Ɛ,γ,λ,α,μ,χ,SDC=1,PPC=0,SFC=1):
    """Fait la simulation de l'épidémie avec P selon avec le modèle complet"""
    S,E,C,I,A,Q,R,M=[P.sains],[P.exposés],[P.contagieux],[P.infectés],[P.asymptomatiques],[P.enQuarantaine],[P.rétablis],[P.morts]
    conf=False
    for _ in range(int(duree/dt)):
        vivants=P.n-P.morts
        if P.infectés+P.enQuarantaine > SDC*vivants or (P.infectés+P.enQuarantaine > SFC*vivants and conf):
            P.propagation_complete(dt,σ*(1-PPC)**2,Ɛ,γ,λ,α,μ,χ)
            conf=True
        else:
            P.propagation_complete(dt,σ,Ɛ,γ,λ,α,μ,χ)
            conf=False 
        S+=[P.sains]
        E+=[P.exposés]
        C+=[P.contagieux]
        I+=[P.infectés]
        A+=[P.asymptomatiques]
        Q+=[P.enQuarantaine]
        R+=[P.rétablis]
        M+=[P.morts]
    return [S,E,C,I,A,Q,R,M]




"""Graphique"""
def graphique_complet(simulation,mod,dt):
    """Affiche l'évolution de l'épidémie en fonction du temps"""
    if mod=="SIR": S,I,R=simulation
    elif mod=="SEIR": S,E,I,R=simulation
    elif mod=="SEIR+": S,E,C,I,A,Q,R,M=simulation
    temps=[t*dt for t in range(len(S))]
    totalInfectés=[I[t]+Q[t] for t in range(len(S))]

    plt.plot(temps,S,color="green",label="Sains")
    if mod=="SEIR+":
        plt.plot(temps,E,color="orange",label="Exposés")
        plt.plot(temps,C,color="#ff7b00",label="Contagieux")
        plt.plot(temps,totalInfectés,color="purple",label="Total infectés")
        plt.plot(temps,I,'--',color="purple",label="Infectés")
        plt.plot(temps,A,color='red',label="Asymptomatiques")
        plt.plot(temps,R,color="blue",label="Rétablis")
        plt.plot(temps,M,color="black",label="Morts")
    else:
        if mod=="SEIR": plt.plot(temps,E,color="orange",label="Exposés")
        plt.plot(temps,I,color="purple",label="Infectés")
        plt.plot(temps,R,color="blue",label="Rétablis")

    plt.title("Évolution de l'épidémie dans le temps")
    plt.xlabel('Temps (en jours)')
    plt.ylabel('Nombre de personnes')
    plt.legend()

    plt.show()




"""Exemple d'utilisation du code"""
# P=population(1000,infectés=5)
# S=simulation_complete(P,150,1/10,3/8,1/3,1/2,1/8,0.25,0.02/8)
# graphique_complet(S,"SEIR+",1/10)
