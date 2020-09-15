import random as rd
import matplotlib.pyplot as plt

def initier_population(n,r=1000):
    return [[rd.randint(0,r) for i in range(n)],[rd.randint(0,r) for i in range(n)]]

def initier_population_old(n,r=1000): #échanger en deux listes de x et de y
    return [(rd.randint(0,r),rd.randint(0,r)) for i in range(n)]

def afficher_population(P):
    X,Y=[],[]
    for p in P:
        x,y=p
        X+=[x]
        Y+=[y]
    plt.plot(X,Y,'.')
    plt.show()

def déplacer(P,m=1):
    for i in range(len(P[0])):
        P[0][i]+=m*2*(rd.random()-0.5)
        P[1][i]+=m*2*(rd.random()-0.5)

def déplacerv2(P,m=1):
    for i in range(len(P[0])):
        P[0][i]+=m*2*(rd.random()-0.5)
        P[1][i]+=m*2*(rd.random()-0.5)

def animer(P,frames=100):
    for i in range(frames):
        déplacer(P)
        plt.plot(P[0],P[1],'.')
    plt.pause(0.1)
    plt.show()

def animerv2(P,m=1,frames=100):
    anim,=plt.plot(P[0],P[1],'.')
    for i in range(frames):
        déplacer(P,m)
        anim.set_xdata(P[0])
        anim.set_ydata(P[1])
        plt.pause(0.02)
    plt.show()



P=initier_population(25,50)
animerv2(P)


#P=initier_population(100,100)
#animer(P)