




class Plateau:

    """Classe définissant les attributs (variables) et les methodes associées au plateau:

    """
    """
    Attributs :
        CouleurQuiJoue : c est la couleur qui doit jouer, 1 pour blanc ; 2 pour noir
        CouleurQuiNeJouePas  : c est l'autre couleur , 1 pour blanc ; 2 pour noir
        List_Coups : c'est la liste de coups possibles sous forme de tupples : (a,b,i,j) pion qui joue de (a,b) vers (i,j)
        jeu[x][y] : c est la couleur du pion placé en (x,y) , 1 pour blanc ; 2 pour noir, 0 pour vide
        FinDePartie : int : = 1 ou 2 (couleur du vainqueur) lorsque la partie est finie sinon =-1

    Méthodes publiques :
        Joue(x,y,a,b): joue le coup du pion (x,y) jusqu'à (a,b). Tous les attributs sont mis à jour après chaque coup joué
        Modifie_Attribus(jeu,couleurQuiJoue,FinDePartie) : permet de modifier
              les 5 attributs de l'objet en donnant une nouvelle valeur à :
             " jeu,couleurQuiJoue,FinDePartie"
        Copie_jeu(): retourne une copie profonde de l'attribut jeu


    """






    def __init__(self,jeu=None ,couleurQuiJoue=1,FinDePartie=-1):
        """constructeur
        """
        self.jeu=[[0] *10  for _ in range(10)]
        self.Modifie_Attribus(jeu,couleurQuiJoue,FinDePartie)

    def Copie_jeu(self):
        """
         retourne une copie profonde de l'attribut jeu
        """
        copie=[[0] *10  for _ in range(10)]
        for i in range(10) : copie[i]=self.jeu[i][:] #plus rapide que list.copy
        return copie

    def Modifie_Attribus(self,jeu,couleurQuiJoue,FinDePartie):
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




        self.List_Coups=[]
        self.__Calcul_List_Coups()


    def Joue(self,x,y,a,b):
        """méthode public : joue un coup de (x,y) à (a,b) si c est possible
        """
        if (x,y,a,b) in self.List_Coups==False : return
        self.jeu[a][b]=self.CouleurQuiJoue
        self.jeu[x][y]=0

        if abs(a-x)>1 :#prise
            i=(a+x)//2
            j=(b+y)//2
            self.jeu[i][j]=0





        if (b==9 and self.CouleurQuiJoue==2)or (b==0 and self.CouleurQuiJoue==1):
            self.FinDePartie=self.CouleurQuiJoue

        else :
            self.CouleurQuiJoue=self.CouleurQuiNeJouePas
            self.CouleurQuiNeJouePas=self.jeu[a][b]
            self.__Calcul_List_Coups()
            if not(self.List_Coups) : self.FinDePartie=self.CouleurQuiNeJouePas #perd car ne peut plus jouer




    def __Calcul_List_Coups_Qui_Prennent(self,i,j) :
        """
         methode privée : calcul la liste des coups pour (i,j) qui prennent, sous forme d une list de tupples (x,y,a,b)
        """
        list=[]
        if self.jeu[i][j]!=self.CouleurQuiJoue : return list

        if i<=7 :
           if j<=7 and self.jeu[i+1][j+1]==self.CouleurQuiNeJouePas and self.jeu[i+2][j+2]==0 : list.append((i,j,i+2,j+2))
           if j>=2 and self.jeu[i+1][j-1]==self.CouleurQuiNeJouePas and self.jeu[i+2][j-2]==0 : list.append((i,j,i+2,j-2))

        if i>=2 :
           if j<=7 and self.jeu[i-1][j+1]==self.CouleurQuiNeJouePas and self.jeu[i-2][j+2]==0 : list.append((i,j,i-2,j+2))
           if j>=2 and self.jeu[i-1][j-1]==self.CouleurQuiNeJouePas and self.jeu[i-2][j-2]==0 : list.append((i,j,i-2,j-2))

        return list

    def __Calcul_List_Coups_Qui_Prennent_Pas(self,i,j) :
        """
         methode privée : calcul la liste des coups pour (i,j) qui ne prennent pas, sous forme d une list de tupples (x,y,a,b)
        """
        list=[]
        if self.jeu[i][j]!=self.CouleurQuiJoue : return list

        if self.CouleurQuiJoue==1 : sens=-1
        else : sens=+1

        if i<=8 :
           if ((j+sens<=9) and (j+sens>=0)) and self.jeu[i+1][j+sens]==0 : list.append((i,j,i+1,j+sens))


        if i>=1 :
            if (j+sens<=9) and (j+sens>=0) and self.jeu[i-1][j+sens]==0 : list.append((i,j,i-1,j+sens))

        return list
    def __Calcul_List_Coups(self) :
        """
         methode privée : calcul la liste des coups sous forme d une list de tupples (x,y,a,b)
        """
        prise=False
        list=[]

        for i in range(10):
            for j in range(10):
               if self.jeu[i][j]==self.CouleurQuiJoue :
                    listPrise=self.__Calcul_List_Coups_Qui_Prennent(i,j)
                    if not(listPrise) : #list vide
                        if prise==True : continue
                        list+=self.__Calcul_List_Coups_Qui_Prennent_Pas(i,j)

                    else : #il y a des prises
                        if prise==False :
                            prise=True
                            list=[]
                        list+=listPrise


        self.List_Coups=list


