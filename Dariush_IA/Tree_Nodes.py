#UCT : Upper Confidence Bound

from random import randint

from  Dariush_IA.MTC import*


import math


#Cette classe représente un noeud d'un arbre
class TreeNode():

    epsilon = 1e-6

    def __init__(self,index,coup):

        """
          ici children c est la liste des coups possibles
          coup : c est le coup qu on va choisir parmi les children =
          self.CouleurQuiJoue c est la couleur qui va jouer le coup
          CouleurQuiNeJouePas : l autre couleur
          Nbre_De_Coups : c est le nbre de children qui correspond au nbre de coups


          on fait de la mise a jour ponctuelle , lorsque plateau arrive ds un children il doit etre ds cet état

          index indique la profondeur du noeud, 0 etant le pere

        """


        #self.debug=False

        self.coup=coup
        self.FinDePartie=-1 #permetra de savoir si ce noeud est une fin de partie:

        self.index=index


        self.children=[]  #TreeNode[] children#ce sont tous le fils de ce noeud, c'est un tableau, qui est null au depart par defaut (pas de fils),on lui associe laliste des coups
        self.nVisits=0
        self.totValue=0
        self.NbreDeFilsPasEncoreVisites=0
        self.poids=0






    def Joue_Les_Coups_Et_mets_A_jour_Les_Attributs_de_Plateau(self,Pt,List_noeuds):
        """
          on joue tous lescoups de la liste et on mets a jour pLATEAU POUR LA PR2PARATION   au MTC
        """
        if self.FinDePartie>0 :
            return # c est une fin de partie pas d extension

        if self.index>0 :

            couleur=List_noeuds[0][0]#le 1er element de cette liste donne la couleur qui doit jouer, ensuite c est les coups

            for i in range(1,self.index+1):
                if  Pt.jeu[List_noeuds[i][0]][List_noeuds[i][1]]!=couleur :
                    print("bug joue un coup a index",self.index, "couleur=",Pt.jeu[List_noeuds[i][0]][List_noeuds[i][1]],"coup:",List_noeuds[i][0]," ",List_noeuds[i][0])
                Pt.Joue_sans_mise_a_jour(List_noeuds[i][0], List_noeuds[i][1], List_noeuds[i][2], List_noeuds[i][3],couleur)



                if couleur==1 : couleur=2
                else : couleur=1
            Pt.Modifie_Attribus(Pt.jeu,couleur,-1,None,None)


    def expand(self,Pt) :#ici va chercher le nbre de coups et creer la liste de coups et donc le nombre de chifrens. A faire

        """*ici on mets a jour le plateau en jouant tous les coups
        puis on cree la liste de coups possibles et donc le nbre de chidren

        """
        if self.FinDePartie>0 :
            return # c est une fin de partie pas d extension

       # self.Joue_Les_Coups_Et_mets_A_jour_Les_Attributs_de_Plateau(Pt,List_noeuds)

        if Pt.FinDePartie>0 :
            self.FinDePartie=Pt.FinDePartie
            return # c est une fin de partie pas d extension

        if Pt.Nbre_De_Coups==0 : #cas ou on ne peut pas jouer normalement pas possible ! a voir
           print('bug car cherche a s etendra alors qu il n y a plus de coups')


           coup_fils=(-1,-1,-1,-1)

           return


        self.NbreDeFilsPasEncoreVisites=Pt.Nbre_De_Coups#c est le nbre de fils qu on va devoir visités



       #ça va creer une liste de 5 fils
        for i in range( self.NbreDeFilsPasEncoreVisites) :

            coup_fils=Pt.List_Coups[i]

            self.children.append(TreeNode(self.index+1,coup_fils))
            if Pt.Nbre_De_Coups>1 : self.children[i].poids=calculPoids(Pt,i)



    #retourne un objet treenode en sortie
    def SelectionneFilsMeilleurValeur(self,List_noeuds_precedents) :#en sortie j ai l objet des fils qui a le plus grand uct , c est  un objet de type TreeNode
        #TreeNode selected = null
        selected=None


        """
         elif self.index==0 and List_noeuds_precedents[0][0]==2:
                min=1000000
                for c in  self.children :

                   if  c.nVisits<min :
                       selected = c
                       min=c.nVisits
        """
        if ( self.NbreDeFilsPasEncoreVisites>0) and List_noeuds_precedents[0][0]==1:
                max=0

                for c in  self.children :

                     if (c.nVisits==0) and (c.poids>0) :
                          if c.poids>max :
                            max=c.poids
                            selected=c

                if max!=0 :
                    self.NbreDeFilsPasEncoreVisites-=1
                else :
                       nbre=0
                       nbHasard=randint(1,self.NbreDeFilsPasEncoreVisites)#trouve un nbre de 1 à self.NbreDeFilsPasEncoreVisites
                       for c in  self.children :

                           if (c.nVisits==0):
                             nbre+=1
                             if (nbre==nbHasard):
                                 selected = c
                                 self.NbreDeFilsPasEncoreVisites-=1
                                 break


        elif ( self.NbreDeFilsPasEncoreVisites>0):
            nbre=0
            nbHasard=randint(1,self.NbreDeFilsPasEncoreVisites)#trouve un nbre de 1 à self.NbreDeFilsPasEncoreVisites
            for c in  self.children :
            #for (TreeNode c : children) :
              if (c.nVisits==0):
                  nbre+=1
                  if (nbre==nbHasard):
                       selected = c
                       self.NbreDeFilsPasEncoreVisites-=1
                       break

            #if self.debug==True : print("coups de feuille ")

        else:



            bestValue = -1




            """
            TESTS sur l influence de la valeur de csteFrequence (valeur théorique=2)
             tests à 15 000 noeuds:
              BLANC: 1   NOIR:racine(2)   résultats = 7/3
              BLANC: racine(2)   NOIR:1   résultats = 7/3           pas de difference entre 1 et 2 ds la racine
              BLANC: racine(16)   NOIR:racine(2)  résultats = 2/8   2 c est mieux que 16
              BLANC: racine(2)   NOIR:racine(0.8)  résultats = 1/9    0.8 c est bcp mieux que 2
              BLANC: racine(0.8)   NOIR:racine(0.8)  résultats = 5/5  à 0.8 les couleurs sont équilibrées mais ça peut passe
              BLANC: racine(0.8)   NOIR:racine(0.8)  résultats =7/3   pas tjs equilibré, blanc semble avantagé
              BLANC: racine(0.8)   NOIR:racine(0)  résultats =6/0       il fo pas mettre 0 sinon joue tres mal
              BLANC: racine(0.4)   NOIR:racine(0.8)  résultats =8/2        0.4 semble mieux que 0.8
              BLANC: racine(0.8)   NOIR:racine(0.4)  résultats =5/5
              BLANC: racine(0.4)   NOIR:racine(0.2)  résultats =4/6        0.2 semble mieux que 0.4
              BLANC: racine(0.2)   NOIR:racine(0.4)  résultats =6/4        0.2 mieux que 0.4
              BLANC: racine(0.02)   NOIR:racine(0.2)  résultats =          blanc joue mal , j ai pas été au bout
              BLANC: racine(0.1)   NOIR:racine(0.2)  résultats=0/5        0.1 joue tres mal devant 0.2
              BLANC: racine(0.2)   NOIR:racine(0.3)  résultats =8/2      02 semble mieux que  0.3
              BLANC: racine(0.3)   NOIR:racine(0.2)  résultats =6/4   0.2 semble un peu mieux que 0.3

              bilan : à 15000 noeuds 0.2 l emporte légèrement sur 0.4 qui l emporte légèrement sur 0.8

              TEST a 30 000 noeuds
              BLANC: racine(0.8)   NOIR:racine(0.2)  résultats =6/4
              BLANC: racine(0.2)   NOIR:racine(0.8)  résultats =5/5  léger avantage pour 0.8 devant 0.2 en 30 000 noeuds

              BLANC: racine(0.8)   NOIR:racine(0.4)    resultat =2/8   0.4 ecrabouille 0.8
              BLANC: racine(0.4)   NOIR:racine(0.8)    resultat =6/4   0.4 ecrabouille 0.8

              vainqueur : 0.4 (faudrait tester 0.6........)

               TEST a 30 000 noeuds Nouvelle version
               BLANC: racine(2)   NOIR:racine(0.4)    resultat =2/8
               BLANC: racine(0.4)   NOIR:racine(2)    resultat =8/2
               BLANC: racine(0.8)   NOIR:racine(0.4)    resultat =6/4
              BLANC: racine(0.4)   NOIR:racine(0.8)    resultat =5/5

            couleur=List_noeuds_precedents[0][0]#a supprimer juste pour les tests
            if couleur==1 :
                csteFrequence=0.4
            else :
                csteFrequence=0.8
            """


            csteFrequence=0.8 #en theorie la bonne valeur est racine(2) maison peut essayer des variantes
            #if List_noeuds_precedents[0][0]==2:if self.index<=1 : csteFrequence=100 marche pas
            #if self.index==0 :
                 # print()
                 # print()
            for c in  self.children :


                        #normalement c.nVisits neput pas etre nul car avant on joue tous les coups non visités en debut d appel de fonction

                        #if c.nVisits==0 : #ps encore de visits, inutile de faire le calcul avec la formule (trop long) on mets un grand nombre avec de l aleatoire ça suffit
                             #uctValue =256+randint(0,5)
                        #else :
                uctValue = c.totValue / (c.nVisits) +math.sqrt(csteFrequence*math.log( self.nVisits) / (c.nVisits )) +randint(0,5)* TreeNode.epsilon

                #if self.index==0 :print(c.coup,"  uct=",uctValue)


                    #uctValue = c.totValue / (c.nVisits + TreeNode.epsilon) +math.sqrt(csteFrequence*math.log( self.nVisits+1) / (c.nVisits +TreeNode.epsilon)) +randint(0,5)* TreeNode.epsilon#j ai mis 2 devt la racine pour tester, à voir...........
                 # small random number to break ties randomly in unexpanded nodes

                if (uctValue > bestValue) :
                    selected = c
                    bestValue = uctValue

            #if bestValue==-1 : print("bug best value")


        List_noeuds_precedents[self.index+1]=selected.coup #important le noeud qu on selectionne est associé a un coup et on doit garder a jour la list des coups
        #if self.debug==True : print("coups  =",selected.coup,"  nbre de visits = ",selected.nVisits, "a index=",self.index)





        return selected

    def SelectionneFilsMeilleurPoids(self) :#en sortie j ai l objet des fils qui a le plus grand poids , c est  un objet de type TreeNode
        #on ne s occupe pas de la partie "visites", que de la partie poit de la valur UCT
        selected=None

        bestValue = -1



        for c in  self.children :
                if c.nVisits==0 :
                    uctValue =0

                else : uctValue = c.totValue / (c.nVisits)

                if (uctValue > bestValue) :
                    selected = c
                    bestValue = uctValue

        #if bestValue==-1 : print("bug best value")



        return selected

    #@return True si ce noeud est une feuille, cad un noeud terminal (c'est une feuille si il n'a pas de fils donc si children == null)
    def CeNoeudEstUneFeuillef(self) :
        #return children == null
        if not(self.children) :
            return True
        else :
            return False




    def JoueLeCoupXY_faitMiseAjourDesAttribus_Et_retourne_couleur_Gagnant(self,Pt,joue):

       """
        #ATTENTION le calcul de cette valeur res ds cette fonction doit être fait pour optimiser ordi !
        #par la suite , pour joueur on prendra l inverse de cette valeur pour tenir compte diu fait que joueur veut minimiser cette valeur !



        #on joue le coup de ce noeud si on passe pas puis on finit aleatoirement
        Attention en sortie la valeur de platau n a plus rien a voir, c est la fin de partie


        ici on a deja rejouer tous les coups precedents ds expands, on rejoue seulement le dernier coup associé a ce noeud
       """

       if joue:
           Pt.Joue_Mise_A_Jour_Attributs(self.coup[0],self.coup[1],self.coup[2],self.coup[3])

       if Pt.FinDePartie>0 :
          self.FinDePartie=Pt.FinDePartie
          return  Pt.FinDePartie



       couleur_Gagne=JoueUnePartieAleatoirement(Pt)


       return couleur_Gagne




    def IncrementeVisitsEtTotValue(self,value):
         """
         on incremente la visite et la valeur,on regarde juste a index=1 si le coup,est pas debile..
         """
         self.nVisits+=1

         """
            ci dessous doit permettre d eviter les sacrifices debiles a index 1 juste bon a eloigner l horizon en cas de perte
            il fof aire une ir=teration jusqu a 3
            coup debile pour ordi =
                -coup qui prend pas a index=1
                -suivi d un coups qui prends a index=2
                -suivi d un coup qui prends pas a index=3
         """
         if (self.index==1 and value==1) and abs(self.coup[0]-self.coup[2])==1 :#coup qui prend pas a index=1
                    if len(self.children)>0 and abs(self.children[0].coup[0]-self.children[0].coup[2])!=1 : #coup qui prend  a index=2
                        """
                          si un filsprends et que ordi reprends pas derriere alors le coup a index=1 était débile et juste un sacrifice
                        """
                        for c in  self.children :
                            if len(c.children)==0 : break #on doit attendre d avoir etudier les coups a index 3 pour trancher si c est un coup debile
                            if  abs(c.children[0].coup[0]-c.children[0].coup[2])==1 : #coup a index=3 qui prends pas
                                  value=0.9 #on met un malus de 0.1 pour sacrifice debile
                                  break


         self.totValue += value



