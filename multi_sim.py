
def multiSim(nbSim,nbPrcs,n,dim,infectés,confinés,duree,dt,pas,r,σ,Ɛ,γ,λ,α,μ,χ,SDC,SFC):
    if nbSim%nbPrcs!=0:
        print("Erreur : nbSim n'est pas un multiple de nbPrcs !")
    q=nbSim//nbPrcs
    for e in [n,dim,infectés,confinés,duree,pas,r,σ,Ɛ,γ,λ,α,μ,χ,SDC,SFC]: e=str(e)
    for i in range(nbPrcs):
        file=open('sim'+str(i)+'.py','w')
        file.write('from modlPhysiq import *\n')
        file.write("multiSimulationDansCsv({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17})".format(str(q*i),str(q*i+q),n,dim,infectés,confinés,duree,dt,pas,r,σ,Ɛ,γ,λ,α,μ,χ,SDC,SFC))
        file.close()

multiSim(64,8,100,31,2,60,200,1/10,0.4,1,1,3,5,14,0.4,0.005,1/22,0.25,0.12)