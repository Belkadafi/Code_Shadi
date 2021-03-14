#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      boissac
#
# Created:     25/09/2019
# Copyright:   (c) boissac 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import random as r

from multiprocessing import Process,  Array
import os

"""
from threading import Thread

try :
    from Dariush_IA.Cythonoutils import *
    print("Dariush 64 bits")

except :

    from Dariush_IA.outils import *
    print("Dariush 32 bits")
"""
def TriElageOuMultipliePourMTC(Plateau) :
    nombre=Plateau.Nbre_De_Coups
    for i in range(Plateau.Nbre_De_Coups):



        if PasDautreProches(Plateau.List_Coups[i][2],Plateau.List_Coups[i][3],Plateau.CouleurQuiNeJouePas,Plateau.jeu):
        #on augmente sa probabilité car coup fort
             if Plateau.CouleurQuiJoue==2 :
                 if Plateau.List_Coups[i][3]==8 :#"c est lemeilleur coup, car gagne le coup d apres, inutile d aller plus loin"

                      if i!=0: Plateau.List_Coups[0]=Plateau.List_Coups[i]
                      Plateau.Nbre_De_Coups=1

                      return

             else :
                 if Plateau.List_Coups[i][3]==1 :#"c est lemeilleur coup, car gagne le coup d apres, inutile d aller plus loin"
                      if i!=0: Plateau.List_Coups[0]=Plateau.List_Coups[i]
                      Plateau.Nbre_De_Coups=1
                      return

             #coup fort on l ajoute pour augmenter sa probabilité
             Plateau.List_Coups[nombre]=Plateau.List_Coups[i]
             nombre+=1

    Plateau.Nbre_De_Coups=nombre


def calculPoids(Plateau,num) :

        if PasDautreProches(Plateau.List_Coups[num][2],Plateau.List_Coups[num][3],Plateau.CouleurQuiNeJouePas,Plateau.jeu):

             if Plateau.CouleurQuiJoue==2 :
                 return Plateau.List_Coups[num][3]#8 :#" 8 c est lemeilleur coup, car gagne le coup d apres, inutile d aller plus loin"


             else :
                 return 9-Plateau.List_Coups[num][3] #:#"8 c est lemeilleur coup, car gagne le coup d apres, inutile d aller plus loin"



        return 0




def TriElageOuMultipliePourMTC(Plateau) :
    nombre=Plateau.Nbre_De_Coups
    for i in range(Plateau.Nbre_De_Coups):

        if Plateau.CouleurQuiJoue==1 :
           if Plateau.List_Coups[i][3]>2 : continue
        elif  Plateau.List_Coups[i][3]<7 : continue

        if PasDautreProches(Plateau.List_Coups[i][2],Plateau.List_Coups[i][3],Plateau.CouleurQuiNeJouePas,Plateau.jeu):
        #on augmente sa probabilité car coup fort
             if Plateau.CouleurQuiJoue==2 :
                 if Plateau.List_Coups[i][3]==8 :#"c est lemeilleur coup, car gagne le coup d apres, inutile d aller plus loin"

                      if i!=0: Plateau.List_Coups[0]=Plateau.List_Coups[i]
                      Plateau.Nbre_De_Coups=1

                      return

             else :
                 if Plateau.List_Coups[i][3]==1 :#"c est lemeilleur coup, car gagne le coup d apres, inutile d aller plus loin"
                      if i!=0: Plateau.List_Coups[0]=Plateau.List_Coups[i]
                      Plateau.Nbre_De_Coups=1
                      return

             #coup fort on l ajoute pour augmenter sa probabilité
             Plateau.List_Coups[nombre]=Plateau.List_Coups[i]
             nombre+=1

    Plateau.Nbre_De_Coups=nombre

def PasDautreProches(x,y,autre,jeu):
    """
      couleur n a pas d ennemis sur les cotés ou devant
      pos forte
    """


    if x<=7 and jeu[x+2][y]==autre : return False
    if x>=2 and jeu[x-2][y]==autre : return False
    if autre==1 : #noir joue

            if x<=8 and jeu[x+1][y+1]==autre : return False
            if x>=1 and jeu[x-1][y+1]==autre : return False

    else : #blanc joue
            if x<=8 and jeu[x+1][y-1]==autre : return False
            if x>=1 and jeu[x-1][y-1]==autre : return False

    return True







def JoueUnePartieAleatoirement(Plateau):
    """joue la partie aleatoirement et retourne la couleur du vainqueur
       Attention les attribus sont modifiés en sortie
    """


    while Plateau.FinDePartie<=0 :

        #si 1er coup gagnant inutile de jouer on quitte

        if Plateau.CouleurQuiJoue==2 :
                  if Plateau.List_Coups[0][3]==9 : return 2
        elif Plateau.List_Coups[0][3]==0 : return 1


        if Plateau.Nbre_De_Coups>1 :
           TriElageOuMultipliePourMTC(Plateau)

        if Plateau.Nbre_De_Coups==1 :
            Plateau.Joue_Mise_A_Jour_Attributs(Plateau.List_Coups[0][0],Plateau.List_Coups[0][1],Plateau.List_Coups[0][2],Plateau.List_Coups[0][3])
        else :

            n=r.randint(0,Plateau.Nbre_De_Coups-1)
            coup=Plateau.List_Coups[n]
            Plateau.Joue_Mise_A_Jour_Attributs(coup[0],coup[1],coup[2],coup[3])

    return Plateau.FinDePartie


def JoueXPartiesAleatoirement(Plateau,x,couleur) :
    """joue x parties aleatoirement et retourne le nombre de fois ou couleur a gagné
        Les attribus ne sont pas  modifiés en sortie
    """
    NbreVictoires=0
    Tamponjeu=[[0] *10  for _ in range(10)]
    TamponFindepartie=-1

    for j in range(10) : Tamponjeu[j]=Plateau.jeu[j][:]
    TamponCouleurQuiJoue=Plateau.CouleurQuiJoue




    for n in range(x):

        resultat=JoueUnePartieAleatoirement(Plateau)

        if resultat==couleur : NbreVictoires+=1
        Plateau.Modifie_Attribus(Tamponjeu,TamponCouleurQuiJoue,TamponFindepartie,None,None)


    return NbreVictoires



def MTCParallelisable(Plateau,Plateau_Depart,X,couleur,depart,fin,TableauPartage) :
    """
      Joue x parties aleatoirement pour chaque coup, regarde le nbre de victoires associés a chacun de ces coups
      et choisis le coup qui donne le plus de victoires à couleur
    """




    Nbre_Parties_joues=0
    #Poids=[0]*len(Plateau.List_Coups)
    NbreVictoires=[0]*Plateau.Nbre_De_Coups




    nombre_Parties_Par_Coups=X//Plateau.Nbre_De_Coups+1

   # for i in range(len(Plateau.List_Coups)) :
    for i in range(depart,fin):


         coup=Plateau.List_Coups[i]




         Plateau.Joue_Mise_A_Jour_Attributs(coup[0],coup[1],coup[2],coup[3])

         Nbre_Parties_joues+=nombre_Parties_Par_Coups

         NbreVictoires[i]=JoueXPartiesAleatoirement(Plateau,nombre_Parties_Par_Coups,couleur)

         #print("j ai joué",coup[0],coup[1],coup[2],coup[3],"pour une victoire de ",NbreVictoires[i])

         Plateau.Modifie_Attribus(Plateau_Depart.jeu,Plateau_Depart.CouleurQuiJoue,Plateau_Depart.FinDePartie,None,None)


    max=-1
    N=0
    for i in range(depart,fin):

        #print("Debugage coup MTC  ",Plateau.List_Coups[i],"   pour un nbre de victoires de ",NbreVictoires[i], " sur ",nombre_Parties_Par_Coups, " pour un total de ",Nbre_Parties_joues," parties jouées")
        #print("victoire de ",i,"est =",NbreVictoires[i])
        if NbreVictoires[i]>max :
            max=NbreVictoires[i]
            N=i

    coup=Plateau.List_Coups[N]
    #print(Plateau.List_Coups)
    #print("coup MTC numero ",N," ",coup,"   pour un nbre de victoires de ",max, " sur ",nombre_Parties_Par_Coups, " pour un total de ",Nbre_Parties_joues," parties jouées")


    TableauPartage[0]=coup[0]
    TableauPartage[1]=coup[1]
    TableauPartage[2]=coup[2]
    TableauPartage[3]=coup[3]

    TableauPartage[4]=max





def Algo_Monte_Carlo(Plateau,Plateau_Depart,X,couleur,Multi_Process):
    arr=[]#list des reponses de processus

    #coup=MTC(Plateau,Plateau_Depart,X,couleur)
    #if coup[0]>1 : return coup



    coup=(0,0,0,0)


    "nbre de coups>1 verifié en amont"


    nbre_cpu=os.cpu_count()//2 #car compte les threads, et y en a 2 par coeurs normalement)
    if nbre_cpu<1 : nbre_cpu=1

    if Multi_Process==0:
        nbre_cpu=1


    #if Plateau.CouleurQuiJoue==2 : Multi_Process=0


    if nbre_cpu<=1 :
        """
            on ne lance pas de processus

        """
        #print("Aucun processus lancé  ")

        arr.append([0,0,0,0,0])
        MTCParallelisable(Plateau,Plateau_Depart,X,couleur,0,Plateau.Nbre_De_Coups,arr[0])

    else :
        """
            Lancement des processus

        """
        #print("nbre de cpu : ",nbre_cpu)
        X=X*nbre_cpu

        if nbre_cpu>Plateau.Nbre_De_Coups :
            saut=1
            modulo=0
            nbre_cpu=Plateau.Nbre_De_Coups


        else :
            saut=Plateau.Nbre_De_Coups//nbre_cpu
            modulo=Plateau.Nbre_De_Coups%nbre_cpu


        depart=0
        fin=depart+saut
        if modulo>0 :
            fin+=1
            modulo-=1

        g=[] #list des processus*





        for i in range(nbre_cpu):
           #print("creation processus ",i)
           arr.append(Array('i', range(5)))
           g.append(Process(target=MTCParallelisable, args=(Plateau,Plateau_Depart,X,couleur,depart,fin,arr[i])))

       #g.append(Algothread(Plateau_Depart,X,couleur,depart,fin))



           depart=fin
           fin=fin+saut
           if modulo>0 :
               fin+=1
               modulo-=1


        for i in range(nbre_cpu) :
            #print("Lancement processus ",i)
            g[i].start()

        for i in range(nbre_cpu) :
            #print("Fin processus ",i)
            g[i].join()







    max=-1
    numprocessus=0
    for i in range(nbre_cpu) :
    #doit etre apres la fermeture du processsu .join !!!!
        """
        if g[i].max>max :
            max=g[i].max
            numprocessus=i
            coup=g[i].coup
        """
        if arr[i][4]>max :
            max=arr[i][4]
            numprocessus=i
            coup=tuple(arr[i][:4])

    print("coupMTC=",coup," processus :",numprocessus," poids=",max)







    return coup


def main():
    pass

if __name__ == '__main__':
    main()
"""
def MTC(Plateau,Plateau_Depart,X,couleur) :




    Nbre_Parties_joues=0
    #Poids=[0]*len(Plateau.List_Coups)
    NbreVictoires=[0]*Plateau.Nbre_De_Coups




    nombre_Parties_Par_Coups=X//Plateau.Nbre_De_Coups+1

   # for i in range(len(Plateau.List_Coups)) :
    for i in range(Plateau.Nbre_De_Coups):


         coup=Plateau.List_Coups[i]




         Plateau.Joue_Mise_A_Jour_Attributs(coup[0],coup[1],coup[2],coup[3])

         Nbre_Parties_joues+=nombre_Parties_Par_Coups

         NbreVictoires[i]=JoueXPartiesAleatoirement(Plateau,nombre_Parties_Par_Coups,couleur)

         Plateau.Modifie_Attribus(Plateau_Depart.jeu,Plateau_Depart.CouleurQuiJoue,Plateau_Depart.FinDePartie,None,None)


    max=-1
    N=0
    for i in range(Plateau.Nbre_De_Coups):

        #print("Debugage coup MTC  ",Plateau.List_Coups[i],"   pour un nbre de victoires de ",NbreVictoires[i], " sur ",nombre_Parties_Par_Coups, " pour un total de ",Nbre_Parties_joues," parties jouées")

        if NbreVictoires[i]>max :
            max=NbreVictoires[i]
            N=i

    coup=Plateau.List_Coups[N]
    print("coup MTC numero ",N,"   pour un nbre de victoires de ",max, " sur ",nombre_Parties_Par_Coups, " pour un total de ",Nbre_Parties_joues," parties jouées")



    return coup


"""
"""
class Algothread(Thread):



    def __init__(self,Plateau_Depart,X,couleur,depart,fin):
        Thread.__init__(self)
        self.Plat=Plateau_Dariush(Plateau_Depart.jeu,Plateau_Depart.CouleurQuiJoue,Plateau_Depart.FinDePartie)
        self.coup=(0,0,0,0)
        self.max=0
        self.X=X
        self.couleur=couleur
        self.depart=depart
        self.fin=fin
        self.Plateau_Depart=Plateau_Depart


    def run(self):


        Nbre_Parties_joues=0

        NbreVictoires=[0]*self.Plat.Nbre_De_Coups




        nombre_Parties_Par_Coups=self.X//self.Plat.Nbre_De_Coups+1


        for i in range(self.depart,self.fin):


             coup=self.Plat.List_Coups[i]




             self.Plat.Joue_Mise_A_Jour_Attributs(coup[0],coup[1],coup[2],coup[3])

             Nbre_Parties_joues+=nombre_Parties_Par_Coups

             NbreVictoires[i]=JoueXPartiesAleatoirement(self.Plat,nombre_Parties_Par_Coups,self.couleur)

             #print("j ai joué",coup[0],coup[1],coup[2],coup[3],"pour une victoire de ",NbreVictoires[i])

             self.Plat.Modifie_Attribus(self.Plateau_Depart.jeu,self.Plateau_Depart.CouleurQuiJoue,self.Plateau_Depart.FinDePartie,None,None)


        self.max=-1
        N=0
        for i in range(self.depart,self.fin):

            #print("Debugage coup MTC  ",Plateau.List_Coups[i],"   pour un nbre de victoires de ",NbreVictoires[i], " sur ",nombre_Parties_Par_Coups, " pour un total de ",Nbre_Parties_joues," parties jouées")
            #print("victoire de ",i,"est =",NbreVictoires[i])
            if NbreVictoires[i]>self.max :
                self.max=NbreVictoires[i]
                N=i

        self.coup=self.Plat.List_Coups[N]
        #print(Plateau.List_Coups)
        print("coup MTC numero ",N," ",self.coup,"   pour un nbre de victoires de ",self.max, " sur ",nombre_Parties_Par_Coups, " pour un total de ",Nbre_Parties_joues," parties jouées")

"""

