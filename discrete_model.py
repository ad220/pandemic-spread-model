import random as rd
import matplotlib.pyplot as plt

def initier_population(n,r=1000):
    return [[rd.randint(0,r) for i in range(n)],[rd.randint(0,r) for i in range(n)],[0 for i in range(n)],[0 for i in range(n)],[r]]


def afficher_population(P):
    X,Y=[],[]
    for p in P:
        x,y,=p
        X+=[x]
        Y+=[y]
    plt.plot(X,Y,'.')
    plt.show()


def déplacer(P,m=1):
    b=P[4][0]
    for i in range(len(P[0])):
        P[0][i]+=m*2*(P[2][i]-0.5)
        if P[0][i] > b : P[0][i]=b
        elif P[0][i] < 0 : P[0][i]=0

        P[1][i]+=m*2*(P[3][i]-0.5)
        if P[1][i] > b : P[1][i]=b
        elif P[1][i] < 0 : P[1][i]=0

        P[2][i]+=0.2*rd.randint(-1,1)
        if P[2][i] > 1 : P[2][i]=1
        elif P[2][i] < -1 : P[2][i]=-1

        P[3][i]+=0.2*rd.randint(-1,1)
        if P[3][i] > 1 : P[3][i]=1
        elif P[3][i] < -1 : P[3][i]=-1


def animer(P,m=0.15,frames=1000,fr=0.01):
    anim,=plt.plot(P[0],P[1],'.')
    for i in range(frames):
        déplacer(P,m)
        anim.set_xdata(P[0])
        anim.set_ydata(P[1])
        plt.pause(fr)
    plt.show()

def animer_pre(P,frames=1000,fr=0.01,m=0.15):
    anim,=plt.plot(P[0],P[1],'.')
    X,Y=[],[]
    for i in range(frames):
        déplacer(P,m)
        X+=[P[0]]
        Y+=[P[1]]
        print(P[0])
    print(X)
    for i in range(frames):
        anim.set_xdata(X[i])
        anim.set_ydata(Y[i])
        plt.pause(fr)
    plt.show()



P=initier_population(25,50)
#animer_pre(P)
