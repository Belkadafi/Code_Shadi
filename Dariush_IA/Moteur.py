#import plateau

from  Dariush_IA.MTC import*
from  Dariush_IA.UCT import*
import time

chercheVersion=False
numVersion=0

while chercheVersion==False :
 try :
    if numVersion==0 :
        from Dariush_IA.CythonPythonX64_374.Cythonoutils import *
        print("lib C PythonX64_3.7.4 chargee")
    elif numVersion==1 :
        from Dariush_IA.CythonPythonX64_369.Cythonoutils import *
        print("lib C PythonX64_3.6.9 chargee")
    elif numVersion==1 :
        from Dariush_IA.CythonPythonX64_366.Cythonoutils import *
        print("lib C PythonX64_3.6.6 chargee")
    elif numVersion==1 :
        from Dariush_IA.CythonPythonX64_357.Cythonoutils import *
        print("lib C PythonX64_3.5.7 chargee")
    elif numVersion==1 :
        from Dariush_IA.CythonPythonX64_349.Cythonoutils import *
        print("lib C PythonX64_3.4.9 chargee")
    elif numVersion==1 :
        from Dariush_IA.CythonPythonX64_337.Cythonoutils import *
        print("lib C PythonX64_3.3.7 chargee")
    elif numVersion==1 :
        from Dariush_IA.CythonPythonX64_326.Cythonoutils import *
        print("lib C PythonX64_3.2.6 chargee")
    elif numVersion==1 :
        from Dariush_IA.CythonPythonX64_314.Cythonoutils import *
        print("lib C PythonX64_3.1.4 chargee")
    elif numVersion==1 :
        from Dariush_IA.CythonPythonX64_301.Cythonoutils import *
        print("lib C PythonX64_3.0.1 chargee")
    else :
        from Dariush_IA.outils import *
        print("Aucune lib C chargee")

    chercheVersion=True
 except : numVersion+=1


def Trouve_Un_Coup(choix,Plateau_Depart,Nbre_simulations,Multi_Process):
    Debut=time.time()

    if len(Plateau_Depart.List_Coups)==1 :
        coup=Plateau_Depart.List_Coups[0]
        return coup



    Plateau=Plateau_Dariush(Plateau_Depart.jeu,Plateau_Depart.CouleurQuiJoue,Plateau_Depart.FinDePartie)
    if Plateau.Nbre_De_Coups==1 :#le calcul des coups n est pas le même ici. Si ya une solgagnante y a qu un coup
        coup=Plateau.List_Coups[0]
        return coup

    if choix==1:
         coup=Algo_Monte_Carlo(Plateau,Plateau_Depart,Nbre_simulations,Plateau_Depart.CouleurQuiJoue,Multi_Process)

    else :
        coup=Algo_UCT(Plateau,Nbre_simulations,Multi_Process)

    Fin=time.time()
    temps=int(Fin-Debut)

    print('coup joue : ',coup,' En : ',temps,' s')
    return coup

