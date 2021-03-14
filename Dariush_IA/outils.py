





class case():

    """
    caracteristique d une case :
    - self x et self y  ses coordonnées
    - self.voisinPrise : liste detupples (a,b,c,d) donnant la position du voisin (a,b) et de la position finale en cas de prise (c,d)
    - self.voisin : liste detupples (a,b) donnant la position du voisin (a,b)

    """

    def __init__(self,x,y):
          self.x=x
          self.y=y
          self.voisinPrise=self.__Calcul_List_des_Tupples_de_voisins_prises(x,y)
          self.voisin = self.__Calcul_List_des_Tupples_de_voisins(x,y)  #self.voisin[0] list des tupples de postions possibles si Blanc ; self.voisin[1] list des tupples de postions possibles si NOIR ;


    def __Calcul_List_des_Tupples_de_voisins_prises(self,i,j) :
        """
         methode privée : calcul la liste des tupples de prises
        """
        list=[]


        if i<=7 :
           if j<=7  : list.append((i+1,j+1,i+2,j+2))
           if j>=2  : list.append((i+1,j-1,i+2,j-2))

        if i>=2 :
           if j<=7 : list.append((i-1,j+1,i-2,j+2))
           if j>=2 : list.append((i-1,j-1,i-2,j-2))

        return list


    def __Calcul_List_des_Tupples_de_voisins(self,i,j) :
        """
         methode privée : calcul la liste des tupples de voisins ou on peut jouer pour blanc list[0] et noir[0]
        """
        #list=[]*2 ne marche pas
        list=[[]  for _ in range(2)]


        if i<=8 :
           if j<=8  : list[1].append((i+1,j+1))
           if j>=1  : list[0].append((i+1,j-1))

        if i>=1 :
           if j<=8 : list[1].append((i-1,j+1))
           if j>=1 : list[0].append((i-1,j-1))

        return list




class Plateau_Dariush:

    """Classe définissant les attributs (variables) et les methodes associées au plateau:

    """
    """
    Attributs :
        CouleurQuiJoue : c est la couleur qui doit jouer, 1 pour blanc ; 2 pour noir
        CouleurQuiNeJouePas  : c est l'autre couleur , 1 pour blanc ; 2 pour noir
        List_Coups : c'est la liste de coups possibles sous forme de tupples : (a,b,i,j) pion qui joue de (a,b) vers (i,j)
        Nbre_De_Coups : c est le nbre de coups ds la liste précédente
        jeu[x][y] : c est la couleur du pion placé en (x,y) , 1 pour blanc ; 2 pour noir, 0 pour vide
        FinDePartie : int : = 1 ou 2 (couleur du vainqueur) lorsque la partie est finie sinon =-1

    Méthodes publiques :
        Joue(x,y,a,b): joue le coup du pion (x,y) jusqu'à (a,b). Tous les attributs sont mis à jour après chaque coup joué
        Modifie_Attribus(jeu,couleurQuiJoue,FinDePartie) permet de modifier tous les attributs de l'objet

    """






    def __init__(self,jeu=None ,couleurQuiJoue=1,FinDePartie=-1):
        """constructeur
        """
        self.jeu=[[0] *10  for _ in range(10)]

        #self.case=[[]  for _ in range(10)]for x in range(10):for y in range(10):self.case[x].append(case(x,y))



        self.Nbre_De_Coups=0


        self.Pion=[]
        self.PionGagnant=[]#pions a une ligne du bord
        for i in range(10) : self.Pion.append((0,0))
        for i in range(5) : self.PionGagnant.append((0,0))
        self.List_Coups=[]
        for i in range(40) : self.List_Coups.append((0,0,0,0))

        self.Modifie_Attribus(jeu,couleurQuiJoue,FinDePartie,None,None)




    def Modifie_Attribus(self,jeu,couleurQuiJoue,FinDePartie,List_Coups,Nbre_De_Coups):
        """ utilisé tel quel  ds le constructeur
        mais permet par la suite de modifier les attributs de l objet facilement sans avoir a refaire une autre instance... créer un nouvel objet prends plus de temps.
        """

        if jeu is None:
            for i in range(10) :
                for j in range(10) :self.jeu[i][j]=0
            i=0
            while i<10:
                #self.jeu[0+i][7]=1
                self.jeu[0+i][9]=1
                self.jeu[1+i][6]=1
               # self.jeu[1+i][8]=1
              #  self.jeu[0+i][1]=2
                self.jeu[0+i][3]=2
                self.jeu[1+i][0]=2
               # self.jeu[1+i][2]=2
                i+=2
        else :
            for i in range(10) : self.jeu[i]=jeu[i][:] #plus rapide que list.copy


        self.FinDePartie=FinDePartie

        self.CouleurQuiJoue=couleurQuiJoue #blanc commence
        if couleurQuiJoue==1 :
            self.CouleurQuiNeJouePas=2 #noir
        else :
             self.CouleurQuiNeJouePas=1



        if List_Coups is None :

            self.Calcul_List_Coups()
        else :
             self.List_Coups=List_Coups[:]
             self.Nbre_De_Coups=Nbre_De_Coups

        if self.Nbre_De_Coups==0 : self.FinDePartie=self.CouleurQuiNeJouePas #perd car ne peut plus jouer

    def Modifie_Attribus_jeu(self,jeu):

            for i in range(10) : self.jeu[i]=jeu[i][:] #plus rapide que list.copy


    def Modifie_Attribus_Couleur_Qui_Joue(self,couleurQuiJoue,FinDePartie):

        self.CouleurQuiJoue=couleurQuiJoue #blanc commence
        if couleurQuiJoue==1 :
            self.CouleurQuiNeJouePas=2 #noir
        else :
             self.CouleurQuiNeJouePas=1
        self.FinDePartie=FinDePartie

    def Modifie_Attribus_List_Coups(self,List_Coups,Nbre_De_Coups):
        self.List_Coups=List_Coups[:]
        self.Nbre_De_Coups=Nbre_De_Coups



    def Joue_Mise_A_Jour_Attributs(self,x,y,a,b):
        """méthode public : joue un coup de (x,y) à (a,b) si c est possible avec mise a jour des attributs et return True
        """
        #if (x,y,a,b) in self.List_Coups==False : return False
        self.jeu[a][b]=self.CouleurQuiJoue
        self.jeu[x][y]=0
        """
        if abs(a-x)>1 :#prise
            i=(a+x)//2
            j=(b+y)//2
            self.jeu[i][j]=0
        """

        if a>x+1 :
            if b>y :
                self.jeu[x+1][y+1]=0
            else :
                 self.jeu[x+1][y-1]=0

        elif  a<x-1:
                if b>y :
                    self.jeu[x-1][y+1]=0
                else :
                    self.jeu[x-1][y-1]=0

        if (self.CouleurQuiJoue==2 and b==9 )or (self.CouleurQuiJoue==1 and b==0 ):
            self.FinDePartie=self.CouleurQuiJoue

        else :
            self.CouleurQuiJoue=self.CouleurQuiNeJouePas
            self.CouleurQuiNeJouePas=self.jeu[a][b]
            self.Calcul_List_Coups()
            if self.Nbre_De_Coups==0 : self.FinDePartie=self.CouleurQuiNeJouePas #perd car ne peut plus jouer

       # return True



    def Joue_sans_mise_a_jour(self,x,y,a,b,couleur):
        """méthode public : joue un coup de (x,y) à (a,b) si c est possible sans mise a jour des attributs et sant test de verification si le coup est possible
        """

        self.jeu[a][b]=couleur
        self.jeu[x][y]=0
        """
        if abs(a-x)>1 :#prise
            i=(a+x)//2
            j=(b+y)//2
            self.jeu[i][j]=0
        """

        if a>x+1 :
            if b>y :
                self.jeu[x+1][y+1]=0
            else :
                 self.jeu[x+1][y-1]=0

        elif  a<x-1:
                if b>y :
                    self.jeu[x-1][y+1]=0
                else :
                    self.jeu[x-1][y-1]=0


    def Calcul_List_Coups_Qui_Prennent(self,i,j) :
        """
         calcul la liste des coups pour (i,j) qui prennent, sous forme d une list de tupples (x,y,a,b)
        """



        if i<=7 :
           if j<=7 and self.jeu[i+1][j+1]==self.CouleurQuiNeJouePas and self.jeu[i+2][j+2]==0 :
                self.List_Coups[self.Nbre_De_Coups]=(i,j,i+2,j+2)
                self.Nbre_De_Coups+=1
           if j>=2 and self.jeu[i+1][j-1]==self.CouleurQuiNeJouePas and self.jeu[i+2][j-2]==0 :
                self.List_Coups[self.Nbre_De_Coups]=(i,j,i+2,j-2)
                self.Nbre_De_Coups+=1

        if i>=2 :
           if j<=7 and self.jeu[i-1][j+1]==self.CouleurQuiNeJouePas and self.jeu[i-2][j+2]==0 :
                self.List_Coups[self.Nbre_De_Coups]=(i,j,i-2,j+2)
                self.Nbre_De_Coups+=1
           if j>=2 and self.jeu[i-1][j-1]==self.CouleurQuiNeJouePas and self.jeu[i-2][j-2]==0 :
                self.List_Coups[self.Nbre_De_Coups]=(i,j,i-2,j-2)
                self.Nbre_De_Coups+=1




    def Calcul_List_Coups_Qui_Prennent_Pas(self,i,j) :
        """
         methode privée : calcul la liste des coups pour (i,j) qui ne prennent pas, sous forme d une list de tupples (x,y,a,b)
        """




        if self.CouleurQuiJoue==1 :#Blanc joue

          if j>0 :
            if i<9 and self.jeu[i+1][j-1]==0 :
                self.List_Coups[self.Nbre_De_Coups]=(i,j,i+1,j-1)
                self.Nbre_De_Coups+=1



            if i>0  and self.jeu[i-1][j-1]==0 :
                self.List_Coups[self.Nbre_De_Coups]=(i,j,i-1,j-1)
                self.Nbre_De_Coups+=1


        else :#Noir joue


          if j<9 :
            if i<9 and self.jeu[i+1][j+1]==0 :
                self.List_Coups[self.Nbre_De_Coups]=(i,j,i+1,j+1)
                self.Nbre_De_Coups+=1


            if i>0  and self.jeu[i-1][j+1]==0 :
                self.List_Coups[self.Nbre_De_Coups]=(i,j,i-1,j+1)
                self.Nbre_De_Coups+=1






    def Calcul_List_Coups(self) :
        """
         calcul la liste des coups sous forme d une list de tupples (x,y,a,b)
         s il y a un coiup gagnant, ne selectionne que lui
        """
        #global Pion
        self.Nbre_De_Coups=0
        Nbre_De_Pions,Nbre_De_Pions_Ligne_Gagnante=0,0

        if self.CouleurQuiJoue==1:
            ligneGagnante=2
            lignegagnante2=1
            bord=0
            debut=1
        else :
            ligneGagnante=7
            lignegagnante2=8
            bord=9
            debut=0
        """
         on regarde d abord si y a des sols gagnantes, si oui, inutile de chercher les autres coups
        """
        for i in range(debut,debut+9,2) :

               if self.jeu[i][ligneGagnante]==self.CouleurQuiJoue :

                    self.Calcul_List_Coups_Qui_Prennent(i,ligneGagnante)
                    if self.Nbre_De_Coups==0:
                        self.Pion[Nbre_De_Pions]=(i,ligneGagnante)
                        Nbre_De_Pions+=1


        if self.Nbre_De_Coups!=0 : #il y a des coups qui prennent sur la ligne gagnante on  regarde si l un d entre eux arrive au bord
            for i in range (self.Nbre_De_Coups) :
                if self.List_Coups[i][3]==bord: #coup gagnant
                    if i>0 :
                        self.List_Coups[0]=self.List_Coups[i] #ne fonctionne que parceque ce sont des tupples sinon ça ferait pas une bonne copie

                    self.Nbre_De_Coups=1
                    return



        debut=0

        for j in range(10):
          debut=debut^1
          if j!=ligneGagnante :

            for i in range(debut,debut+9,2) :

               if self.jeu[i][j]==self.CouleurQuiJoue :

                    self.Calcul_List_Coups_Qui_Prennent(i,j)
                    if self.Nbre_De_Coups==0:
                           if j!=lignegagnante2 :
                               self.Pion[Nbre_De_Pions]=(i,j)
                               Nbre_De_Pions+=1

                           else :
                                self.PionGagnant[Nbre_De_Pions_Ligne_Gagnante]=(i,j)
                                Nbre_De_Pions_Ligne_Gagnante+=1#pion qui est a une ligne du bord



        if self.Nbre_De_Coups==0:#list vide s il n y a pas de coups qui prennent

            """

        ETUDE DES COUPS QUI PRENNENT PAS
        ON COMMENCE PAR CEUX QUI GAGNENT
             """

            if Nbre_De_Pions_Ligne_Gagnante>0:
                for n in range(Nbre_De_Pions_Ligne_Gagnante):
                    self.Calcul_List_Coups_Qui_Prennent_Pas(self.PionGagnant[n][0],self.PionGagnant[n][1])
                    if self.Nbre_De_Coups!=0: #list pas vide
                #c est une solgagnante inutile d aller plus loin
                         self.Nbre_De_Coups=1
                         return

            if Nbre_De_Pions>0:
                for n in range(Nbre_De_Pions):
                    self.Calcul_List_Coups_Qui_Prennent_Pas(self.Pion[n][0],self.Pion[n][1])


