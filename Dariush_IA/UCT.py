


from  Dariush_IA.Tree_Nodes import*

from multiprocessing import Process,  Array
import os

# selectionnes ce noeud et  cherches ses  fils puis  remontes la valeur du meilleur
def selectAction(RacineDesNoeuds,Plateau,List_noeuds_precedents,profondeurMax) :

        #global profondeurMax,CouleurOrdi,CouleurJoueur


        #List<TreeNode> visited = new LinkedList<TreeNode>()#creation d une liste de type TreeNode

        CouleurOrdi=List_noeuds_precedents[0][0]
        visited=[]
        cur = RacineDesNoeuds  # cur curseur est un objet TreeNode
        #visited.add(RacineDesNoeuds)
        visited.append(RacineDesNoeuds)

       # if nombreUCT==0 : cur.expand(Plateau,List_noeuds_precedents)


        index=0
        #bug=False

        if cur.FinDePartie<0 :

            #cur = cur.SelectionneFilsMeilleurValeur(List_noeuds_precedents)

            #visited.append(cur)

            while (cur.CeNoeudEstUneFeuillef()==False) or (index==0):
                """
                #tant que le noeud courant n'est pas une feuille, on le selectionne
                si le noeud est une feuille, on créé des noeuds pour ses fils avec expand

                """
                index+=1

                cur = cur.SelectionneFilsMeilleurValeur(List_noeuds_precedents)


                #visited.add(cur)
                visited.append(cur)
                """
                if index==-1:
                    if cur.coup==(0,5,1,4) :
                        print()
                        print("Haut d arbre")
                        bug=True
                    else :
                        bug=False

                if bug:
                    print(cur.coup)
                """

        """
          on joue tous les coups de la liste pour mettre a jour plateau

        """

        cur.Joue_Les_Coups_Et_mets_A_jour_Les_Attributs_de_Plateau(Plateau,List_noeuds_precedents)


        """
          ici c est une feuille (pas de fils)
          -soit on y est deja arrivé, ds ce cas on lui cree des fils et on selctionne le meilleur fils
          -soiton l a jamais evalué ,ds ce cas on l evalue

        """
        if cur.FinDePartie>0 :
                 gagnantMTC =cur.FinDePartie
        elif cur.nVisits!=0 : #deja etudié donc on cree des fils et on selectionne
            #on   crée les fils du noeud cur
                 cur.expand(Plateau)
                 newNode = cur.SelectionneFilsMeilleurValeur(List_noeuds_precedents)#newNode ça  sera le fils de plus grand uct
                 #if bug: print("dernier coup=",newNode.coup)
                 gagnantMTC = newNode.JoueLeCoupXY_faitMiseAjourDesAttribus_Et_retourne_couleur_Gagnant(Plateau,True)
                 visited.append(newNode)

        else : #coup de feuille non etudié , on le joue et on l'évalue
                 #if bug: print("dernier coup=",cur.coup)
                 gagnantMTC = cur.JoueLeCoupXY_faitMiseAjourDesAttribus_Et_retourne_couleur_Gagnant(Plateau,False)



        prof=len(visited)
        if (prof>profondeurMax[0]): profondeurMax[0]=prof


        if gagnantMTC==CouleurOrdi : #lorsque ordi gagne ça doit faire perdre joueur et reciproquement
            Valeur_ordi,Valeur_joueur=1,0
        else :
            Valeur_ordi,Valeur_joueur=0,1



        numero_noeud=0
        for node in visited:
             if numero_noeud<=1 : #les 2 remiers noeuds c est ordi apres ça alterne
                couleur=CouleurOrdi
             else :
                if couleur==1 : couleur=2
                else : couleur=1
             numero_noeud+=1




             if couleur==CouleurOrdi :

                node.IncrementeVisitsEtTotValue(Valeur_ordi)
             else : node.IncrementeVisitsEtTotValue(Valeur_joueur)






             #print(node.Pt.FinDePartie)
             #print(node.Pt.Nbre_De_Coups)





def Affiche_le_nbre_de_visites_de_chaque_fils(NoeudPapa) :
               for c in NoeudPapa.children :

                    print(" coup= ",c.coup," pour ",c.nVisits," visites sur ",NoeudPapa.nVisits," pour une valeur=",c.totValue / (c.nVisits))

                    uct=c.totValue / (c.nVisits) +math.sqrt(0.8*math.log(NoeudPapa.nVisits) / (c.nVisits ))
                    print("uct=",uct)

                    #c.totValue / (c.nVisits) +math.sqrt(csteFrequence*math.log( self.nVisits) / (c.nVisits ))



def Affiche_la_branche_principale_jusquaubout(NoeudPapa,Plat) :




        cur = NoeudPapa

        index=0;


        while (cur.CeNoeudEstUneFeuillef()==False) and (cur.nVisits>2): #tant que le noeud courant n'est pas une feuille, on le selectionne
            index=index+1
            cur = cur.SelectionneFilsMeilleurPoids()

            print("index=",index," coup=",cur.coup," pour ",cur.nVisits," visites pour une valeur=",cur.totValue / (cur.nVisits))

            Plat.Joue_Mise_A_Jour_Attributs(cur.coup[0],cur.coup[1],cur.coup[2],cur.coup[3])






def UCTParallelisable(Plateau,NbreDeNoeudUCT,depart,fin,TableauPartage) :
        """
        choisis le coup qui donne le plus de victoires UCT à couleur

        """
        affiche=False
        profondeurMax=[0]
        """
        if num==2:
            print('depart=',depart," fin=",fin)
            affiche=True
        """
        """on modifie la liste des coups
        pour n etudier que ceux de ce processus
        """

        Plateau.Nbre_De_Coups=0

        for i in range(depart,fin):
           Plateau.List_Coups[Plateau.Nbre_De_Coups]=Plateau.List_Coups[i]
           Plateau.Nbre_De_Coups+=1



        TamponCouleurQuiJoue=Plateau.CouleurQuiJoue
        TamponFinDePartie=Plateau.FinDePartie
        TamponNbre_De_Coups=Plateau.Nbre_De_Coups
        TamponJeu=[[0] *10  for _ in range(10)]
        for i in range(10) : TamponJeu[i]=Plateau.jeu[i][:]
        TamponList_Coups=[]
        TamponList_Coups=Plateau.List_Coups[:]

        List_noeuds_precedents=[]
        for i in range(80) : List_noeuds_precedents.append((0,0,0,0))

        CouleurOrdi = Plateau.CouleurQuiJoue#1 c est blanc ; 2 c est noir
        if (CouleurOrdi==1) :
            CouleurJoueur =2
        else : CouleurJoueur=1






        List_noeuds_precedents[0]=(CouleurOrdi,0,0,0) #le 1er tupple donne des renseignements sur la couleur  qui doitjouer





        #c est le papa des noeud , il n a pas de pere, que des fils qui sont les coups joués
        #c est autre couleur qui vient de jouer, donc c est autrecouleur qu on mets a la racine


        NoeudDebut=TreeNode(0,List_noeuds_precedents[0])
        NoeudDebut.expand(Plateau)
        #if (CouleurOrdi==1) : NbreDeNoeudUCT=100000



        for i in range(NbreDeNoeudUCT) :
            #print("descente d'arbre numero :",i)

            selectAction(NoeudDebut,Plateau,List_noeuds_precedents,profondeurMax)



            Plateau.Modifie_Attribus(TamponJeu,TamponCouleurQuiJoue,TamponFinDePartie,TamponList_Coups,TamponNbre_De_Coups)


        if (affiche==True) :Affiche_le_nbre_de_visites_de_chaque_fils(NoeudDebut)

        #debug=False
        #if debug==True :
             #print("DEBUGAGE")
             #Affiche_la_branche_principale_jusquaubout(NoeudDebut, Plateau)
             #Plateau.Modifie_Attribus(TamponJeu,TamponCouleurQuiJoue,TamponFinDePartie,TamponList_Coups,TamponNbre_De_Coups)

             #print("FIN dU DEBUGAGE")

       # Affiche_la_branche_principale_jusquaubout(NoeudDebut);mt.copiePlateau1DansPlateau2(tampon_plateau,mt.plateau);



        NoeudFilsChoisiAuDebut=NoeudDebut.SelectionneFilsMeilleurPoids() #on cherche le meilleur fils, c est lui le bon coup
        coup=NoeudFilsChoisiAuDebut.coup



        #print("coupUCTChoisiParceprocessus=",coup," Prof= ",profondeurMax[0]," pour ",NoeudFilsChoisiAuDebut.nVisits," visites sur ",NbreDeNoeudUCT," pour une valeur=",NoeudFilsChoisiAuDebut.totValue / (NoeudFilsChoisiAuDebut.nVisits))

        TableauPartage[0]=coup[0]
        TableauPartage[1]=coup[1]
        TableauPartage[2]=coup[2]
        TableauPartage[3]=coup[3]

        TableauPartage[4]=int(10000*NoeudFilsChoisiAuDebut.totValue / (NoeudFilsChoisiAuDebut.nVisits))

        #return coup




def Algo_UCT(Plateau,NbreDeNoeudUCT,Multi_Process):
    arr=[]#list des reponses de processus

    coup=(-1,0,0,0)


    #if Plateau.CouleurQuiJoue==1 : Multi_Process=0
    #if Plateau.CouleurQuiJoue==2 : NbreDeNoeudUCT=90000


    "nbre de coups>1 verifié en amont"


    nbre_cpu=os.cpu_count()//2 #car compte les threads, et y en a 2 par coeurs normalement)
    if nbre_cpu<1 : nbre_cpu=1

    if Multi_Process==0:
        nbre_cpu=1




    if nbre_cpu<=1 :
        """
            on ne lance pas de processus

        """
        #print("Aucun processus lancé ")

        arr.append([0,0,0,0,0])
        UCTParallelisable(Plateau,NbreDeNoeudUCT,0,Plateau.Nbre_De_Coups,arr[0])

    else :
        """
            Lancement des processus

        """
        #nbre_cpu=1

        NbreDeNoeudUCT= NbreDeNoeudUCT*nbre_cpu
        #print("nbre de cpu : ",nbre_cpu," Nbre de noeuds UCT=",NbreDeNoeudUCT)





        if nbre_cpu>Plateau.Nbre_De_Coups :
            saut=1
            modulo=0
            nbre_cpu=Plateau.Nbre_De_Coups


        else :
            saut=Plateau.Nbre_De_Coups//nbre_cpu
            modulo=Plateau.Nbre_De_Coups%nbre_cpu

        #print("nbre de coups=",Plateau.Nbre_De_Coups)
        #print("nbre de coups=",Plateau.Nbre_De_Coups, "list=",Plateau.List_Coups)
        depart=0
        fin=depart+saut
        if modulo>0 :
            fin+=1
            modulo-=1

        g=[] #list des processus*

        NbreDeNoeudUCTParcoup=1+NbreDeNoeudUCT//Plateau.Nbre_De_Coups

        for i in range(nbre_cpu):
         #  print("creation processus ",i)
           arr.append(Array('i', range(5)))
           NbreDeNoeudUCTParProcessus=NbreDeNoeudUCTParcoup*(fin-depart)
           g.append(Process(target=UCTParallelisable, args=(Plateau,NbreDeNoeudUCTParProcessus,depart,fin,arr[i])))



           depart=fin
           fin=fin+saut
           if modulo>0 :
               fin+=1
               modulo-=1


        "nbre de coups>1 verifié en amont"



        for i in range(nbre_cpu) :
          #  print("Lancement processus ",i)
            g[i].start()

        for i in range(nbre_cpu) :
           # print("Fin processus ",i)

            g[i].join()






    max=-1
    numprocessus=0
    for i in range(nbre_cpu) :
    #doit etre apres la fermeture du processsu .join !!!!
        if arr[i][4]>max :
            max=arr[i][4]
            numprocessus=i
            coup=tuple(arr[i][:4])
    print("coupUCT=",coup," processus :",numprocessus,"/",nbre_cpu," poids=",max," Noeuds=",NbreDeNoeudUCT)







    return coup



