import random as rd
import matplotlib.pyplot as plt

def gauss(n,p):
    L=[]
    for i in range(n):
        c=1
        while rd.random()>p:
            c+=1
        L+=[c]
        # print(str(100*i/n)+"%")
    # plt.plot([t for t in range(max(L))],[L.count(t) for t in range(max(L))])
    # plt.show()
    return sum(L)/n

def gauss_simple(n,p):
    L=[rd.randint(1,p) for _ in range(n)]
    plt.plot([t for t in range(p)],[L.count(t) for t in range(p)])
    plt.show()

def gauss_2(n,centre,precs):
    L=[]
    for i in range(n):
        L+=[int(gauss(precs,centre))]
        print(str(100*i/n)+"%")
    plt.plot([n for n in range(max(L))],[L.count(t) for t in range(max(L))])
    plt.show()

gauss_2(100000,1/80,25)
# breakpoint()