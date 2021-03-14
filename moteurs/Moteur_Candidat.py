import Utils.class_plateau

"""
   Objet LePlateau :
        les attributs et méthodes de l'objet LePlateau vous sont
        accessibles par LePlateau. suivi du nom de l'attribu ou de la méthode

    Attributs :
        CouleurQuiJoue : c est la couleur qui doit jouer, 1 pour blanc ; 2 pour noir
        CouleurQuiNeJouePas  : c est l'autre couleur , 1 pour blanc ; 2 pour noir
        List_Coups : c'est la liste de coups possibles sous forme de tupples
            (a,b,i,j) pion qui joue de (a,b) vers (i,j)
        jeu[x][y] : c est la couleur du pion placé en (x,y) ,
            1 pour blanc ; 2 pour noir, 0 pour vide
        FinDePartie : = 1 ou 2 (couleur du vainqueur) lorsque la partie est finie sinon =-1

    Méthodes publiques :
        Joue(x,y,a,b): joue le coup du pion (x,y) jusqu'à (a,b).
             Tous les attributs sont mis à jour après chaque coup joué
        Modifie_Attribus(jeu,couleurQuiJoue,FinDePartie) : permet de modifier
              les 5 attributs de l'objet en donnant une nouvelle valeur à :
             " jeu,couleurQuiJoue,FinDePartie"
        Copie_jeu(): retourne une copie profonde de l'attribut jeu

"""


def Trouve_Un_Coup(LePlateau):
    """
     doit retourner un tupple (a,b,c,d) qui donne la position de depart a,b
     et la position d arrivée c,d du pion joué.
     L'objet LePlateau a tous les attriubuts mis à jour
    """

    coup=(0,0,0,0)


    return coup
