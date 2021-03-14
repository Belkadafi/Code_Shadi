import  tkinter as Tki
import Utils.class_plateau
from tkinter.messagebox import *
from tkinter import filedialog
import os
import importlib
import Dariush_IA.Moteur as Dar
from threading import Thread
import time

pygame_active=True
try :
  from pygame import mixer
except :
  print('Pour avoir du son, installe Pygame')
  pygame_active=False


class Ecoute_Moteur(Thread):

    """
    Thread lancé au debut qui ecoute a intervalle de temps regulier (0.1 s)
    et qui lance le moteur selectionné automatiquement
    si c est à lui de jouer
    """

    def __init__(self):
        Thread.__init__(self)
        self.Lancement_Moteur=False #indique si un moteur est en train de calculer un coup



    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        global SynchroAffiche
        n=0

        while En_cours_De_Partie :


            n+=1
            if LePlateau.FinDePartie<=0:
              if  (GMJ.JoueurBlanc!="Humain" and LePlateau.CouleurQuiJoue==1)or (GMJ.JoueurNoir!="Humain" and LePlateau.CouleurQuiJoue==2):


                self.Lancement_Moteur=True #permet de desactiver les evenments graphiques type menu, ou clic durant la reflexion IA


                #Thread_Chrono.run()#pour forcer le calcul du temps au debut

                if LePlateau.CouleurQuiJoue==1 : nom=GMJ.JoueurBlanc
                else : nom=GMJ.JoueurNoir

                Canevas.configure(cursor="watch")



                if nom=="Dariush-MTC" :
                     Multi_Process=GMJ.Multi_Process
                     Multi_Process=GMJ.Multi_Process.get()
                     coup=Dar.Trouve_Un_Coup(1,LePlateau,Dariush_MTC_Nbre_Simulations,Multi_Process)
                elif nom=="Dariush-UCT" :
                     Multi_Process=GMJ.Multi_Process.get()
                     coup=Dar.Trouve_Un_Coup(2,LePlateau,Dariush_UCT_Nbre_Simulations,Multi_Process)

                else :
                     #on transmet par precaution une copie de LePlateau aux moteurs
                    LePlateauMoteur.Modifie_Attribus(LePlateau.jeu,LePlateau.CouleurQuiJoue,LePlateau.FinDePartie)
                    index=GMJ.List_moteurs.index(nom)
                    coup=GMJ.Modules_moteurs[index].Trouve_Un_Coup(LePlateauMoteur)

                Canevas.configure(cursor="hand2")

                if not((coup) in LePlateau.List_Coups ):
                    showerror('ERREUR',"Votre coup "+ str(coup)+" n'est pas autorisé !")
                    GMJ.JoueurBlanc="Humain"
                    GMJ.JoueurNoir="Humain"
                else :
                    LePlateau.Joue(coup[0],coup[1],coup[2],coup[3])
                    if pygame_active and DesactiveSon.get()==0 : son.play() # joue le son
                    global selection,Les_coups_joues,Num_Du_Coup
                    Les_coups_joues[Num_Du_Coup]=coup
                    Num_Du_Coup+=1
                    selection=[0,0,coup[2],coup[3]]
                    affiche()


                self.Lancement_Moteur=False
                TestFinDePartie()
                #Thread_Chrono.run()#pour forcer le calcul du temps à la fin
              else :
               if SynchroAffiche==False : time.sleep(0.1)#var de synchro pour eviter le clignotement

        print('Thread Moteur termine')

class Chrono(Thread):

    """
    Permet de calculer et d afficher les chronomètres de Noir et Blanc
    """

    def __init__(self):
        Thread.__init__(self)
        self.TempsNoir=0
        self.TempsBlanc=0
        self.DerniereCouleurAJouer=1 #Blanc Commence


    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        Debut=time.time()

        while En_cours_De_Partie :


            if LePlateau.FinDePartie>0:
                Debut=time.time()
                self.DerniereCouleurAJouer=1

            elif LePlateau.CouleurQuiJoue==self.DerniereCouleurAJouer :
                Fin=time.time()
                temps=int(Fin-Debut)
                Debut=Fin
                if LePlateau.CouleurQuiJoue==1 : self.TempsBlanc+=temps
                else : self.TempsNoir+=temps
            else :
                 Debut=time.time()
                 self.DerniereCouleurAJouer=LePlateau.CouleurQuiJoue



            try:

                Canevas.create_rectangle(20,60,220,90,fill='grey')
                Canevas.create_text(120, 75, text=str(Thread_Chrono.TempsBlanc)+" s/"+str(Thread_Chrono.TempsNoir)+" s", font="Arial 15 bold italic", fill='white')## le texte est centré en x,y !bold = gras


            except :
                print('Thread chrono termine')
                return

            time.sleep(1)


class Gestion_Moteurs_Joueurs():

    """
    Gestion des moteurs et des joueurs
    importation/supression d un moteur
    liste des moteurs
    affectation d un moteur à noir ou blanc

    """

    def __init__(self):
          self.List_moteurs=[] #list des noms de moteurs
          self.Modules_moteurs=[] #list des modules moteurs importés
          self.JoueurBlanc="Humain"
          self.JoueurNoir="Humain"
          self.rep=os.getcwd() #donne le repertoire courant
          self.Multi_Process=Tki.IntVar()
          self.Multi_Process.set(0) #0 desactuvé ; 1 active tous les coeurs de la machine
          self.ouvrirConfig()
          self.varBlanc = Tki.IntVar()
          self.varBlanc.set(0)
          self.varNoir = Tki.IntVar()
          self.varNoir.set(0)
          self.fenetre_modifs=None
          self.entree =None
          self.choixMoteur=0
          self.Tournoi=-1 #desactivé
          self.ScoreBlanc=0
          self.ScoreNoir=0





    def choixJoueur(self,joueur,x):


        choix=self.List_moteurs[x]

        if joueur==1 :
            GMJ.JoueurBlanc=choix

        else :
            GMJ.JoueurNoir=choix
        affiche()


    def SupprimeMoteur(self,choix):



        self.Initialise_sous_menus_moteurs()
        if self.JoueurBlanc==self.List_moteurs[choix] :
            self.JoueurBlanc="Humain"
        if self.JoueurNoir==self.List_moteurs[choix] :
            self.JoueurNoir="Humain"
        del(self.List_moteurs[choix])
        del(self.Modules_moteurs[choix])

        self.enregistreConfig(False)
        self.ouvrirConfig()
        self.Affiche_sous_menus_moteurs()
        affiche()

    def ImporteMoteur(self):



        rep=self.rep+"\\moteurs"

        try :
           Mafenetre.fichier=filedialog.askopenfilename(initialdir=rep,title="Importer un moteur :") # Afficher la boite de dialogue
           nom=Mafenetre.fichier
           position=1
           while position>0 :
             position = nom.find('/')+1
             nom=nom[position:]

           position = nom.find('.py')
           nom=nom[:position]

        except :
             showerror("Erreur", "Erreur d'ouverture de fichier.")
             return

        #try :


        p=importlib.import_module("moteurs."+nom)
            #print(p)

       # p.Trouve_Un_Coup(LePlateau)

        self.Modules_moteurs.append(p)
        self.List_moteurs.append(nom)

        self.enregistreConfig(False)
        self.ouvrirConfig()
        n=len(self.List_moteurs)-1
        sous_menu_liste_moteurs.add_command(label=nom,command=lambda x=n:self.SupprimeMoteur(x))

        sous_menu_liste_joueurblanc.add_radiobutton(label=nom,value=n+1,variable=self.varBlanc, command=lambda y=1,x=n:self.choixJoueur(y,x))
        sous_menu_liste_joueurnoir.add_radiobutton(label=nom,value=n+1,variable=self.varNoir, command=lambda y=2,x=n:self.choixJoueur(y,x))
        #except :
        #    showerror("Erreur", "Erreur dans votre module moteur. Consultez l'aide.")
         #   return

    def Initialise_sous_menus_moteurs(self):
         sous_menu_liste_joueurblanc.delete(0,len(self.List_moteurs)-1)
         sous_menu_liste_joueurnoir.delete(0,len(self.List_moteurs)-1)
         sous_menu_liste_moteurs.delete(0,len(self.List_moteurs)-3)
    def Affiche_sous_menus_moteurs(self):

        if len(self.List_moteurs)>NbreMoteursDariush+1 :
          for x in range(NbreMoteursDariush+1,len(self.List_moteurs)): sous_menu_liste_moteurs.add_command(label=self.List_moteurs[x],command=lambda choix=x:self.SupprimeMoteur(choix))

        #value est la valeur a donner a variable qd le radiobutton est selectionné
        for x in range(len(self.List_moteurs)):
            if x==1 :
                text="Dariush-Monte-Carlo"
            else : text=self.List_moteurs[x]
            sous_menu_liste_joueurblanc.add_radiobutton(label=text,value=x,variable=self.varBlanc, command=lambda joueur=1,choix=x:self.choixJoueur(joueur,choix))
            sous_menu_liste_joueurnoir.add_radiobutton(label=text,value=x, variable=self.varNoir,command=lambda joueur=2,choix=x:self.choixJoueur(joueur,choix))




    def ouvrirConfig(self):
        global Dariush_MTC_Nbre_Simulations,Dariush_UCT_Nbre_Simulations

        rep=self.rep+ "\\Utils\\config.txt"


        try :



        #ouverture du fichier en lecture
            fichier = open(rep, "r")





            self.List_moteurs=[]
            self.Modules_moteurs=[]
            u=0
            for ligne in fichier:
               position = ligne.find('\n')
               ligne=ligne[:position]
               if u==0 :
                   Dariush_MTC_Nbre_Simulations=int(ligne)
               elif u==1 :
                   Dariush_UCT_Nbre_Simulations=int(ligne)
               elif u==2 :
                    n=int(ligne)
                    self.Multi_Process.set(n)


               elif u>=NbreMoteursDariush+4 : #moteurs eleves
                     p=importlib.import_module("moteurs."+ligne)
                     #print(p)
                   #  p.Trouve_Un_Coup(LePlateau) #pour verifier que lemoteur IA possede la bonne methode
                     self.Modules_moteurs.append(p)
                     self.List_moteurs.append(ligne)
               else :
                     self.Modules_moteurs.append(None)
                     self.List_moteurs.append(ligne)




               #print(ligne,u)
               u+=1

            fichier.close()
        except :

           showinfo('Erreur',"Erreur de lecture du fichier config.")
           self.enregistreConfig(True)


    def enregistreConfig(self,parDefaut):


        rep=self.rep+ "\\Utils\\config.txt"
        if parDefaut==True : #y a eu un bug on remet la liste par defaut.
                self.List_moteurs=[]
                self.Modules_moteurs=[]
                self.List_moteurs.append("Humain")
                self.List_moteurs.append("Dariush-MTC")
                self.List_moteurs.append("Dariush-UCT")
                self.Modules_moteurs.append(None)
                self.Modules_moteurs.append(None)

        try :



            #ouverture du fichier en ecriture
            fichier = open(rep, "w")


            global Dariush_MTC_Nbre_Simulations,Dariush_UCT_Nbre_Simulations
            #on enregistre dabord le nombre de simulations pour dariush montecarlo et dariushuct
            chaine="%i" % (Dariush_MTC_Nbre_Simulations)+"\n"
            fichier.write(chaine)
            chaine="%i" % (Dariush_UCT_Nbre_Simulations)+"\n"
            fichier.write(chaine)

            chaine="%i" % (self.Multi_Process.get())+"\n"
            fichier.write(chaine)


            for i in range(len(self.List_moteurs)):
                      chaine=self.List_moteurs[i]+'\n'
                      fichier.write(chaine)
                # Fermeture du fichier
            fichier.close()
        except :

           showinfo('Erreur',"Erreur d'écriture dans le fichier config.txt.")


    def Nbre_Parties_Auto(self,event):
        longueur=1

        try :
            nbre= str ( self.entree .get())
            longueur=len(nbre)

            nbre=int(nbre)
            if nbre>0:
                #print('ok')
                self.Tournoi=nbre
                self.ScoreBlanc=0
                self.ScoreNoir=0
                self.fenetre_modifs.destroy()

            else :
                 self.entree.delete(0,longueur)

        except :
            print('pas bon')
            self.entree.delete(0,longueur)



    def TournoiAuto(self):

        self.fenetre_modifs = Tki.Toplevel()  ##ouverture fenetre secondaire qui se detruit lors de la fermeture de la fenetre principale
        self.fenetre_modifs.title("Tournoi automatique")
        self.fenetre_modifs.geometry('500x190')
        couleur='#e6e6ff'
        couleur_icone_fenetre="#f6f6f6"
        canvasmodif = Tki.Canvas(self.fenetre_modifs, width=500, height=160, background=couleur, bd=0,relief='flat',highlightcolor='white', cursor="hand2")## parametre en globale sinon pb pour gestion de la souris
        self.entree = Tki.Entry ( self.fenetre_modifs,fg="red", font="Arial 12 bold" )
        self.entree . bind ("<Return >",self.Nbre_Parties_Auto)
        canvasmodif.create_text(150, 30, text="Tournoi Automatique",anchor="w", font="Arial 14 bold", fill="black")## le texte est centré en x,y !bold = gras


        canvasmodif.create_text(50, 80, text="Entrez le nombre de parties automatiques voulu.",anchor="w", font="Arial 12 bold", fill="black")## le texte est centré en x,y !bold = gras

        canvasmodif.create_text(10, 110, text="Les parties seront automatiquement enregistrées sous la forme ",anchor="w", font="Arial 12 bold", fill="black")## le texte est centré en x,y !bold = gras
        canvasmodif.create_text(20, 140, text=" moteur1-moteur2-numéro du vainqueur-numéro de la partie",anchor="w", font="Arial 12 bold", fill="black")## le texte est centré en x,y !bold = gras

        canvasmodif. grid (row =1, column =0, padx =0, pady =0)
        self.entree.grid (row =2, column =0, padx =0, pady =0)
        self.fenetre_modifs . mainloop ()





    def Valider_Nbre_Simulation(self,event):
        global Dariush_MTC_Nbre_Simulations,Dariush_UCT_Nbre_Simulations
        longueur=1
        try :
            nbre= str ( self.entree .get())

            longueur=len(nbre)
            nbre=int(nbre)
            if nbre>=100 and nbre <=100000 :

                if self.choixMoteur==1 :

                     Dariush_MTC_Nbre_Simulations=nbre
                else :
                      Dariush_UCT_Nbre_Simulations=nbre
                self.entree =None
                self.enregistreConfig(False)
                self.fenetre_modifs.destroy()
            else :

                self.entree.delete(0,longueur)

        except :
            print('pas bon')
            self.entree.delete(0,longueur)



    def ModificationMoteurDariush(self,choix):
        self.choixMoteur=choix
        if choix==3 :
            nbre_cpu=os.cpu_count()//2
            if nbre_cpu<=1 :
                showinfo("Multi-core","Votre microprocesseur n'a qu'un seul coeur. Cette option ne peut pas être activée")
                return
            message='Votre microprocesseur a '  + str(nbre_cpu)+' coeurs.' '\n' + '\n'+' Cette option crée ' + str(nbre_cpu)+' programmes IA indépendants'
            message3='\n'+" multipliant ainsi le nombres de simulations par "+str(nbre_cpu)
            message2= '\n'+'\n'+'Attention cette option monopolise les CPUs de votre microprocesseur et peut faire chauffer la carte mère.'+'\n'+'\n'+' Bonne ventilation nécessaire. '
            message4= '\n'+'\n'+"Voulez-vous activer cette option ?"
            reponse=askquestion("Multi-core",message+message3+message2+message4)
            if reponse=='yes' :
                self.Multi_Process.set(1)
            else :
                self.Multi_Process.set(0)
            self.enregistreConfig(False)
            affiche()

            return
        elif choix==1 :
            mot="Dariush-Monte-Carlo"
            valeurMoteur=str(Dariush_MTC_Nbre_Simulations)

        else :
            mot="Dariush-UCT"#Algorithme UCT (Upper Confidence Bound 1 applied to Trees) est un algorithme  Monte Carlo tree search (MCTS)basé sur la formule UCB 1 de Auer, Cesa-Bianchi et Fischer
            valeurMoteur=str(Dariush_UCT_Nbre_Simulations)

        self.fenetre_modifs = Tki.Toplevel()  ##ouverture fenetre secondaire qui se detruit lors de la fermeture de la fenetre principale
        self.fenetre_modifs.title("Modification parametres")
        self.fenetre_modifs.geometry('500x190')
        couleur='#e6e6ff'
        couleur_icone_fenetre="#f6f6f6"
        canvasmodif = Tki.Canvas(self.fenetre_modifs, width=600, height=160, background=couleur, bd=0,relief='flat',highlightcolor='white', cursor="hand2")## parametre en globale sinon pb pour gestion de la souris
        self.entree = Tki.Entry ( self.fenetre_modifs,fg="red", font="Arial 12 bold" )
        self.entree . bind ("<Return >",self.Valider_Nbre_Simulation )
        canvasmodif.create_text(10, 20, text="Nombre de simulations par processus = "+valeurMoteur,anchor="w", font="Arial 12 bold", fill="red")## le texte est centré en x,y !bold = gras


        canvasmodif.create_text(10, 50, text="Pour modifier le nombre de parties simulées dans l'algorithme ",anchor="w", font="Arial 12 bold", fill="black")## le texte est centré en x,y !bold = gras
        canvasmodif.create_text(140, 80, text="de "+mot,anchor="w", font="Arial 12 bold", fill="black")## le texte est centré en x,y !bold = gras

        canvasmodif.create_text(50, 110, text="Entrez un nombre entre 100 et 100 000 puis validez",anchor="w", font="Arial 12 bold", fill="black")## le texte est centré en x,y !bold = gras
        canvasmodif.create_text(100, 140, text=" avec la touche entrée (Return).",anchor="w", font="Arial 12 bold", fill="black")## le texte est centré en x,y !bold = gras

        canvasmodif. grid (row =1, column =0, padx =0, pady =0)

        self.entree.grid (row =2, column =0, padx =0, pady =0)

        self.fenetre_modifs . mainloop ()






def affiche():
     global SynchroAffiche
     decalX=-80
     SynchroAffiche=True #pour eviter le clignotement il faut laisser l affichage se poursuivre jsuq au botu, vis a vis des autres threadfs

     Canevas.delete(Tki.ALL)
     Canevas.create_text(320, 30, text="Jeu de Shadi", font="Arial 40 bold italic", fill='#a6a6e6')## le texte est centré en x,y !bold = gras
     Canevas.create_image(100+decalX,100,anchor = Tki.NW, image=photoplateau)
     Canevas.create_image(480,50,anchor = Tki.NW, image=SUIVANT)
     Canevas.create_image(560,50,anchor = Tki.NW, image=RETOUR)


     Canevas.create_rectangle(0,703,800,727,fill='#e6e6ff',outline='#e6e6ff')
     Canevas.create_text(300, 715, text="Blanc/Noir : "+GMJ.JoueurBlanc+"/"+GMJ.JoueurNoir, font="Arial 16  bold italic", fill='#868686')## le texte est centré en x,y !bold = gras

     Canevas.create_rectangle(20,60,220,90,fill='grey')
     Canevas.create_text(120, 75, text=str(Thread_Chrono.TempsBlanc)+" s/"+str(Thread_Chrono.TempsNoir)+" s", font="Arial 15 bold italic", fill='white')## le texte est centré en x,y !bold = gras

     if GMJ.Tournoi>=0 :
        Canevas.create_rectangle(280,60,360,90,fill='grey')
        Canevas.create_text(320, 75, text=str(GMJ.ScoreBlanc)+" /"+str(GMJ.ScoreNoir), font="Arial 15 bold italic", fill='white')## le texte est centré en x,y !bold = gras




     r=20
     for X in range(10) :
        for Y in range(10):
            if LePlateau.jeu[X][Y]!=0:

                y=52*Y+165
                x=int(52.5*X+165.5)+decalX

                if LePlateau.jeu[X][Y]==1 :

                    Canevas.create_image(x-18,y-20,anchor = Tki.NW, image=PionBlanc)
                else :

                    Canevas.create_image(x-18,y-20,anchor = Tki.NW, image=PionNoir)
              #  Canevas.create_oval(x-r, y-r,x+r, y+r, fill=couleur,outline=couleur)

                if X==selection[0] and Y==selection[1] :
                    Canevas.create_oval(x-5, y-5,x+5, y+5, fill='red',outline='red')
                elif  X==selection[2] and Y==selection[3] :
                    Canevas.create_oval(x-5, y-5,x+5, y+5, fill='blue',outline='blue')

     Canevas.update()
     SynchroAffiche=False

def enregistrefichier():
    if Thread_EM.Lancement_Moteur==True : return #thread d'un moteur IAen cours
    rep=os.getcwd() #donne le repertoire courant
    rep=rep+"\\parties"

    try :


        Mafenetre.fichier=filedialog.asksaveasfilename(title="Enregistrer un fichier Dariush-Shadi :", initialdir=rep,filetypes = [("Fichiers Dariush-Shadi","*.ddus")]) # Afficher la boite de dialogue

        if (( Mafenetre.fichier.find('.ddus')==-1)):
           Mafenetre.fichier=Mafenetre.fichier+".ddus"

        #Mafenetre.fichier=rep+"\\essai.ddus"

        #ouverture du fichier en ecriture
        fichier = open(Mafenetre.fichier, "w")

        for i in range(Num_Du_Coup) :
            chaine=str(Les_coups_joues[i])+"\n"
            fichier.write(chaine)


        fichier.close()
    except :

       showinfo('Erreur',"Erreur d'écriture de fichier.")




def enregistrefichierNom(Nom):
    if Thread_EM.Lancement_Moteur==True : return #thread d'un moteur IAen cours
    rep=os.getcwd() #donne le repertoire courant
    rep=rep+"\\parties\\Tournoi"

    try :



        Mafenetre.fichier=rep+"\\"+Nom+".ddus"

        #ouverture du fichier en ecriture
        fichier = open(Mafenetre.fichier, "w")

        for i in range(Num_Du_Coup) :
            chaine=str(Les_coups_joues[i])+"\n"
            fichier.write(chaine)


        fichier.close()
    except :

       showinfo('Erreur',"Erreur d'écriture de fichier.")









def ouvreunfichier():
    if Thread_EM.Lancement_Moteur==True : return #thread d'un moteur IAen cours

    rep=os.getcwd() #donne le repertoire courant
    rep=rep+"\\parties"

    try :

        Mafenetre.fichier=filedialog.askopenfilename(title="Ouvrir un fichier Dariush-Shadi :", initialdir=rep,filetypes = [("Fichiers Dariush-Shadi","*.ddus")]) # Afficher la boite de dialogue


        #ouverture du fichier en lecture
        fichier = open(Mafenetre.fichier, "r")

        global Num_Du_Coup,Les_coups_joues,LePlateau
        Num_Du_Coup=0
        for ligne in fichier:
            Les_coups_joues[Num_Du_Coup]=eval(ligne)
            Num_Du_Coup+=1

        initialise_sans_affiche_sans_numcoup()
        for i in range(Num_Du_Coup) :
            coup=Les_coups_joues[i]
            LePlateau.Joue(coup[0],coup[1],coup[2],coup[3])

        affiche()

        fichier.close()
    except :

       showinfo('Erreur',"Erreur de lecture de fichier.")



def  ClicSuivantRetour(choix):
     global Num_Du_Coup,Les_coups_joues,LePlateau

     if choix==1 :
        if Num_Du_Coup>0:

            initialise_sans_affiche_sans_numcoup()
            #initialise()
            Num_Du_Coup-=1
            for i in range(Num_Du_Coup) :
                coup=Les_coups_joues[i]
                LePlateau.Joue(coup[0],coup[1],coup[2],coup[3])
            GMJ.JoueurBlanc="Humain"
            GMJ.JoueurNoir="Humain"
            GMJ.varBlanc.set(0)
            GMJ.varNoir.set(0)
            affiche()

     elif choix==2 :
            coup=Les_coups_joues[Num_Du_Coup]
            if coup in LePlateau.List_Coups :
                GMJ.JoueurBlanc="Humain"
                GMJ.JoueurNoir="Humain"
                GMJ.varBlanc.set(0)
                GMJ.varNoir.set(0)
                LePlateau.Joue(coup[0],coup[1],coup[2],coup[3])

                affiche()
                Num_Du_Coup+=1



def TestFinDePartie() :

    gagnant=LePlateau.FinDePartie
    if gagnant<0 : return False

    if gagnant==1 : couleur="Blanc"
    else : couleur="Noir"

    if GMJ.Tournoi>0 :
        Nom=GMJ.JoueurBlanc+"-"+GMJ.JoueurNoir+"-"+couleur+'-'+str(GMJ.Tournoi)
        GMJ.Tournoi-=1
        if gagnant==1 :GMJ.ScoreBlanc+=1
        else : GMJ.ScoreNoir+=1

        enregistrefichierNom(Nom)
        affiche()
        if GMJ.Tournoi>0 :

            initialise()
            return
        else:
            GMJ.Tournoi=-1 #desactive le mode tournoi
            showinfo('Résultats du tournoi','Tournoi terminé ' + '\n' +' Score de Blanc = '+str(GMJ.ScoreBlanc)+'\n' +" Score de Noir = "+str(GMJ.ScoreNoir))


    reponse=askokcancel('Fin de partie',couleur+ " a gagné. Une nouvelle partie ?")

    if reponse==True :
        initialise()

    return True

def Clic(event):
    """ Gestion de l'événement Clic gauche sur la zone graphique """


    x,y=event.x,event.y



    global selection
    decalX=80
    if Thread_EM.Lancement_Moteur==True : return #thread d'un moteur IAen cours

    if y>52 and y<92:
       if x>482 and x<523 :
         ClicSuivantRetour(2)
         return
       if x>563 and x<604 :
         ClicSuivantRetour(1)
         return



    if TestFinDePartie() : return

    x = x+decalX





    Y=(y-140)//52
    X=int((x-140)//52.5)


    if X>9 or X<0 or Y>9 or Y<0 : return


    if selection[0]==0 and selection[1]==0 :
        if LePlateau.jeu[X][Y]!=LePlateau.CouleurQuiJoue :
            if LePlateau.CouleurQuiJoue==1 :
                showinfo('Erreur',"C'est à blanc de jouer.")
            else :
                showinfo('Erreur',"C'est à noir de jouer.")

            return
        selection[0],selection[1]=X,Y
        affiche()


        return

    if (selection[0],selection[1],X,Y) in LePlateau.List_Coups :
        LePlateau.Joue(selection[0],selection[1],X,Y)

        if pygame_active and DesactiveSon.get()==0 : son.play() # joue le son
        global Les_coups_joues,Num_Du_Coup
        Les_coups_joues[Num_Du_Coup]=(selection[0],selection[1],X,Y)
        Num_Du_Coup+=1
        selection=[0,0,X,Y]

        affiche()


        TestFinDePartie()
    else :
        showinfo('Erreur','Coup incorrect ( Rappel : prise obligatoire )')
        selection[0],selection[1]=0,0
        affiche()

def initialise_sans_affiche_sans_numcoup():
    global LePlateau,selection

    LePlateau.Modifie_Attribus(None,1,-1)
    #LePlateau=plateau.Plateau()
    Thread_Chrono.TempsBlanc=0
    Thread_Chrono.TempsNoir=0
    selection=[0,0,0,0]


def initialise():
    global LePlateau,selection,Num_Du_Coup

    LePlateau.Modifie_Attribus(None,1,-1)
    #LePlateau=plateau.Plateau()
    Thread_Chrono.TempsBlanc=0
    Thread_Chrono.TempsNoir=0
    selection=[0,0,0,0]
    Num_Du_Coup=0
    affiche()

def lance_mail():
         mail="prof.boissac@gmail.com"
         os.startfile("mailto:"+mail)
def mise_a_jour():
         adresse_web="https://sites.google.com/view/jeu-shadi/accueil"
         os.startfile(adresse_web)
def affiche_aide() :


    fenetre_resultats = Tki.Toplevel()  ##ouverture fenetre secondaire qui se detruit lors de la fermeture de la fenetre principale
    fenetre_resultats.title("Aide et renseignements divers.")
    fenetre_resultats.geometry('720x400')
    couleur='#e6e6ff'
    couleur_icone_fenetre="#f6f6f6"

    canvas3 = Tki.Canvas(fenetre_resultats, width=700, height=400, background=couleur, bd=0,relief='flat',highlightcolor='white', cursor="hand2")## parametre en globale sinon pb pour gestion de la souris

   # canvas3.create_text(30, 70, text="Tuto sur Youtube : ",anchor="w", font="Arial 15 bold", fill="black")## le texte est centré en x,y !bold = gras

    boutoncontact = Tki.Button(canvas3,bd='6', font="Arial 15 bold",text='Contact',overrelief='groove',bg=couleur_icone_fenetre,command=lance_mail)
    canvas3.create_window(550,230,window=boutoncontact)

    boutonmiseajour = Tki.Button(canvas3,bd='6', font="Arial 15 bold",text='Mise à jour',overrelief='groove',bg=couleur_icone_fenetre,command=mise_a_jour)
    canvas3.create_window(550,30,window=boutonmiseajour)


      #creation de la scroll bar
    defilY = Tki.Scrollbar(fenetre_resultats, orient='vertical', command=canvas3.yview)
    canvas3.configure(scrollregion=(0,0,720, 1390), yscrollcommand= defilY.set)


    ajoutVertical=-20
    canvas3.create_text(10, 50+ajoutVertical, text="Régle du jeu de Shadi : ",anchor="w", font="Arial 15 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 80+ajoutVertical, text="- Les joueurs jouent chacun à leur tour. Les blancs commencent.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 110+ajoutVertical, text="- Chaque pion peut se déplacer d'une case vers l'avant en diagonale.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 140+ajoutVertical, text="- Le joueur qui parvient le premier à atteindre la dernière rangée avec un pion est vainqueur.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 170+ajoutVertical, text="- Si un des joueurs est dans l'impossibilité de jouer il perd la partie.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras

    canvas3.create_text(20, 200+ajoutVertical, text="- Un pion peut en prendre un autre en sautant par dessus un pion adverse. ",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 230+ajoutVertical, text="- La prise peut également s'effectuer en arrière. ",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 260+ajoutVertical, text="- La prise est obligatoire.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras

    ajoutVertical=240
    canvas3.create_text(10, 50+ajoutVertical, text="Créer votre moteur IA : ",anchor="w", font="Arial 15 bold", fill="black")## le texte est centré en x,y !bold = gras

    canvas3.create_text(20, 80+ajoutVertical, text='- Dans le répertoire "moteurs" copier le module "Moteur-Candidat" et renommez le à votre convenance.',anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras

    canvas3.create_text(20, 110+ajoutVertical, text="- La fonction Trouve_Un_Coup() est obligatoire et doit renvoyer un tupple correspondant au coup choisi.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 140+ajoutVertical, text="- En dehors de cette fonction vous êtes libre de faire tout ce que vous voulez.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 170+ajoutVertical, text="- Le tupple coup=(a,b,i,j) donne les coordonnées (a,b) du pion joué et celle de sa case d'arrivée (i,j)",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 200+ajoutVertical, text="- Le paramètre LePlateau est un objet aux propriétés publiques suivantes (voir module plateau):",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(25, 230+ajoutVertical, text=". LePlateau.CouleurQuiJoue : c est la couleur qui doit jouer, 1 pour blanc ; 2 pour noir",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(25, 260+ajoutVertical, text=". LePlateau.CouleurQuiNeJouePas  : c est l'autre couleur",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(25, 290+ajoutVertical, text=". LePlateau.List_Coups : c'est la liste de coups possibles sous forme de tupples : [(a,b,i,j),.....]",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(25, 320+ajoutVertical, text=". LePlateau.jeu[x][y] : c est la couleur du pion placé en (x,y) , 1 pour blanc ; 2 pour noir, 0 pour vide",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(25, 350+ajoutVertical, text=". LePlateau.FinDePartie = 1 ,2 (couleur du vainqueur) ou =-1 lorsque la partie est finie.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 380+ajoutVertical, text="- Une fois créée vous pouvez importer votre moteur dans Dariush-Shadi à l'aide du menu",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 410+ajoutVertical, text="- A partir du menu vous pouvez faire jouer Noir ou Blanc avec les moteurs de votre choix",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 440+ajoutVertical, text="- Les coordonnées vont de (0,0) case en haut à gauche jusqu'à (9,9) en bas à droite.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras


    """
    ajoutVertical=660
    canvas3.create_text(10, 50+ajoutVertical, text="Participer au concours, règles et démarches : ",anchor="w", font="Arial 15 bold", fill="black")## le texte est centré en x,y !bold = gras

    canvas3.create_text(20, 80+ajoutVertical, text="- Notre concours de moteurs IA  est accessible à tous, mais les différentes épreuves et classements se feront ",anchor="w", font="Arial 10 bold", fill="black")
    canvas3.create_text(20, 110+ajoutVertical, text="selon le niveau du candidat : lycéen en première, Terminale, Bac+1,..., hors scolaire, etc.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    ajoutVertical=690
    canvas3.create_text(20, 110+ajoutVertical, text="- Vous envoyez votre module moteur IA à prof.boissac@gmail.com",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 140+ajoutVertical, text="- Sur le mail indiquez : nom/prénom ; niveau scolaire ; établissement fréquenté",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 170+ajoutVertical, text="- Votre moteur doit obligatoirement tourner sur cette interface (langage Python, Cython, C...)",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras

    canvas3.create_text(20, 200+ajoutVertical, text="- Le temps de réflexion est limité à 15 minutes par moteur par partie.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 230+ajoutVertical, text="- Votre moteur ne doit pas systématiquement jouer les mêmes parties (aspect aléatoire).",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras

    canvas3.create_text(20, 260+ajoutVertical, text="- Régulièrement nous ferons concourir les moteurs des candidats.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 290+ajoutVertical, text="- Le classement sera mis à jour et apparaitra sur le site : https://sites.google.com/view/jeu-shadi/accueil ",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 320+ajoutVertical, text="- Aucun prix, juste la satisfaction d'avoir participé et éventuellement d'être le(a) meilleur(e) ! ",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    """


    #ajoutVertical=1000

    ajoutVertical=680
    canvas3.create_text(10, 50+ajoutVertical, text="Les moteurs Dariush : ",anchor="w", font="Arial 15 bold", fill="black")## le texte est centré en x,y !bold = gras

    canvas3.create_text(20, 80+ajoutVertical, text="- Pour tester et entrainer votre moteur, Dariush vous propose 2 moteurs d'entrainement.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 110+ajoutVertical, text="- Dariush-Monte-Carlo : algorithme Monte Carlo ",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 140+ajoutVertical, text="- Dariush-UCT : Algorithme UCT (Upper Confidence Bound 1 applied to Trees) est un algorithme ",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 170+ajoutVertical, text="  Monte Carlo tree search (MCTS)basé sur la formule UCB 1 de Auer, Cesa-Bianchi et Fischer",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 200+ajoutVertical, text="- Vous pouvez faire jouer X parties automatiquement à votre moteur contre Dariush en ",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras
    canvas3.create_text(20, 230+ajoutVertical, text="  selectionnant dans le menu : menu/moteurs/Tournoi automatique.",anchor="w", font="Arial 10 bold", fill="black")## le texte est centré en x,y !bold = gras





    canvas3.create_text(20, 280+ajoutVertical, text="Bonne programmation IA !",anchor="w", font="Arial 20 bold", fill="black")## le texte est centré en x,y !bold = gras



    defilY.grid( row=0, column=1, sticky=Tki.N+Tki.S )
    canvas3.grid(row=0, column=0)



def affiche_licence() :

    global Version
    fenetre_resultats = Tki.Toplevel()  ##ouverture fenetre secondaire qui se detruit lors de la fermeture de la fenetre principale
    fenetre_resultats.title( "Licence Dariush-Shadi version " +Version+ " 2019")
    fenetre_resultats.geometry('1240x300')

    canvas3 = Tki.Canvas(fenetre_resultats, width=1220, height=300, background='#e6e6ff', bd=0,relief='flat',highlightcolor='white')## parametre en globale sinon pb pour gestion de la souris


      #creation de la scroll bar
    defilY = Tki.Scrollbar(fenetre_resultats, orient='vertical', command=canvas3.yview)
    canvas3.configure(scrollregion=(0,0,1240, 1900), yscrollcommand= defilY.set)



    canvas3.create_text(10, 30, text="Software License Agreement ",anchor="w", font="Arial 15 bold", fill="black")


    canvas3.create_text(10, 110, text="1.  Freeware releases." ,anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 130, text="Dariush-Shadi Freeware release can be freely downloaded from http://fred.boissac.free.fr/index.htm web site, or can be found from some Software directories or free cdrom. Use of this software  is not time limited  ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 150, text="nor restricted by usage counter. This release can be used freely only as long as being in a strictly personal context without any lucrative activities.  ",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 180, text="2. Permitted License Uses." ,anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 200, text="Dariush-Shadi Freeware release can be installed and used on one or several computers, while respecting the conditions enumerated at first paragraph for this kind of license (strictly personal context, no multiple users, no networks and in the)",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 220, text="condition that one product instance is actually installed on each computer. This license mode is not applicable to multiple-users and/or network uses. ",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 250, text="3. Restrictions." ,anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 270, text="You may make one copy of the Software in machine-readable form for backup purposes only; provided that the backup copy must include all copyright or other proprietary notices contained on the original. You are not allowed not rent, lease,",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 290, text="lend or sublicense the Software product, neither propose commercial hosting services to third parties using the Software product. You may, however, make a one-time permanent transfer of all of your license rights to the Software to another",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 310, text=" party, provided that: (a) the transfer must include all of the Software, including all its component parts, original media, printed materials and this License; (b) you do not retain any copies of the Software, full or partial, including ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 330, text="copies stored on a computer or other storage device; and (c) the party receiving the Software reads and agrees to accept the terms and conditions of this License The Freeware release can be copied and spreaded without medium limitation ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 350, text=" (internet, cdrom, magazines...), at the condition that the original software packaging has not been changed, altered in any way. Moreover, selling the Freeware release is stricly prohibited whatever the medium used. You are not authorized ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 370, text="to decompile, reverse engineer, dissassemble, modify the software, reduce the software to a human-perceivable form, or create derivative works of the Software or any part thereof.",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 400, text="4. Termination. " ,anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 420, text="This License is effective until terminated. Your rights under this License will terminate automatically without notice if you fail to comply with any term(s) of this License. Upon the termination of this License, you shall ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 440, text="cease all use of the Software and destroy all copies, full or partial, of the Software. ",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 470, text="5. Support and future releases." ,anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 490, text="The software is delivered 'as is' and no upgrade nor modification will be started or done until the next version is released. However, any comment is welcome and can be sent to software author who will reserve the right to make requested ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 510, text="enhancements or corrections for the next release of the product. ",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 540, text="6. Disclaimer of Warranties.  ",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 560, text="You expressly acknowledge and agree that use of the software is at your sole risk and that the entire risk as to satisfactory quality, performance, accuracy and effort is with you. The software is provided 'as is with all faults and without ',  ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 580, text="warranty of any kind. There is no warrant against interference with your enjoyment of the software, that the functions contained in the software will meet your requirements, that the operation of the software will be uninterrupted or error-free,    ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 600, text="or that defects in the software will be corrected. No oral or written information or advice given by the author or an authorized representative shall create a warranty.",anchor="w", font="Arial 8", fill="black")


    canvas3.create_text(10, 630, text="7. Limitation of Liability.",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 650, text="In no event shall the author / seller of the software be liable for personal injury, or any incidental, special, indirect or consequential damages whatsoever, including, without limitation, damages for loss of profits, loss of data, business ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 670, text="interruption or any other commercial damages or losses, arising out of or related to your use or inability to use the software, however caused. Moreover, Dariush-Shadi's author can not be responsible for any problem that could happen ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 690, text="on the computer where Dariush-Shadi is installed, whether or not it is due to Dariush-Shadi, directly or not. ",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 720, text="8. Complete Agreement. ",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 740, text="This License constitutes the entire agreement between the parties with respect to the use of the Software licensed hereunder and supersedes all prior or contemporaneous understandings regarding such subject matter. No amendment to or",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 760, text="modification of this License will be binding unless in writing and signed by the author. Any translation of this License is done for local requirements and in the event of a dispute between the French and any non-French versions,",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 780, text="the French version of this License shall govern This Agreement will terminate automatically, without notice from the author, if the Licensee fails to comply with this Agreement. Licensees who fail to comply with this licence agreement  ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 800, text="will be prosecuted under the maximum extent requested by law.",anchor="w", font="Arial 8", fill="black")


    canvas3.create_text(10, 900, text="Contrat de Licence Logiciel",anchor="w", font="Arial 15 bold", fill="black")




    canvas3.create_text(10, 980, text="1. Version Freeware. ",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 1000, text="La version Freeware de Dariush-Shadi est téléchargeable gratuitement sur Internet depuis le site http://fred.boissac.free.fr/index.htm, ou peut être trouvée via certains annuaires logiciels ou cédéroms gratuits. L’utilisation de  ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1020, text="cette version n’est pas limitée dans le temps ni restreinte par un compteur d’usage. Elle ne peut être utilisée gratuitement que dans un cadre strictement personnel à but non lucratif.",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1040, text=" ",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 1070, text="2. Concession de licence. ",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 1090, text="La version Freeware du logiciel peut être installée et utilisée sur un ou plusieurs ordinateurs, dans le respect des conditions énumérées au paragraphe 1 pour ce type de licence ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1110, text="(contexte strictement personnel, pas d’utilisations réseaux / simultanées) et à condition qu’une instance du produit soit installée sur chaque ordinateur. Ce type de licence n’est pas applicable aux utilisations réseaux et/ou simultanées.",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 1140, text="3. Restrictions.",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 1160, text="Vous ne pouvez réaliser qu'une seule copie du logiciel à des fins exclusives de sauvegarde, à condition que cette copie de sauvegarde reproduise impérativement les informations relatives aux droits d'auteur ou autres droits de propriété  ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1180, text="figurant sur l'original. Vous n'êtes pas autorisé à prêter ou à louer le Produit Logiciel, ni à proposer à des tiers des services d’hébergement commercial à l’aide du Produit Logiciel.Vous pouvez toutefois effectuer le transfert unique et",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1200, text="permanent de tous vos droits  sur le logiciel à une autre partie, à condition : ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1220, text="(a) que ce transfert comprenne la totalité du logiciel, y compris la totalité de ses composants, données d'origine, documents imprimés ainsi que la licence ; (b) que vous ne conserviez aucune copie du logiciel, complète ou partielle,",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1240, text="y compris toute copie stockée sur ordinateur ou toute autre unité de stockage ; et (c) que la partie bénéficiaire prenne connaissance et accepte les termes et conditions de la présente licence. Cette version Freeware peut être diffusée",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1260, text="sans limitation  de média (internet, cédéroms, magazines...), à la condition que le package original ne soit pas modifié ni altéré. De plus, la revente de la version Freeware est strictement interdite quel que soit le moyen utilisé.",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1280, text="Vous n'êtes pas autorisé à reconstituer la logique du Produit Logiciel, à le décompiler, à le désassembler, ou à faire un 'reverse engineering' (ingénierie inverse), à le modifier, ni créer des produits dérivés du logiciel ou de toute partie de ce dernier. ",anchor="w", font="Arial 8", fill="black")


    canvas3.create_text(10, 1310, text="4. Terme de la licence. ",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 1330, text="Cette licence est d'application jusqu'à son terme. Vos droits découlant de cette licence prendront automatiquement fin sans notification de la part de l’auteur si vous ne vous conformez pas à l'une quelconque de ses dispositions.",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1350, text="Dès l'expiration de cette licence, vous serez tenu de cesser toute utilisation du logiciel et de détruire tous les exemplaires, complets ou partiels, dudit logiciel. ",anchor="w", font="Arial 8", fill="black")


    canvas3.create_text(10, 1380, text="5. Support et futures versions.",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 1400, text="Le logiciel est livré 'comme tel' et aucune modification (amélioration et/ou correction) ne sera entreprise jusqu'à la version suivante. Toutefois, les suggestions pourront être envoyées à l’auteur qui pourra s'il le souhaite,",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1420, text="ajouter les fonctionnalités demandées à la nouvelle version du logiciel.",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 1450, text="6. Exclusion de garanties.",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 1470, text="Vous reconnaissez et admettez expressément que l’utilisation du logiciel est à vos risques et périls et que la totalité du risque relatif à la qualité, aux performances, à l’exactitude et au maniement satisfaisants repose sur vous. Le logiciel est fourni ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1490, text="“tel quel”avec tous ses défauts et sans aucune garantie d’aucune sorte. Il n’est nullement garanti l’absence de perturbations lors de votre utilisation du logiciel, que les fonctions contenues dans le logiciel correspondront à vos besoins, que le ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1510, text="fonctionnement du logiciel sera ininterrompu ou exempt d’erreur, ou que tout défaut du logiciel sera corrigé. Aucune information ni aucun conseil communiqués verbalement ou par écrit par ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1530, text="l’auteur ou par l’un de ses représentants autorisés ne pourra constituer une garantie. ",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 1560, text="7. Limitation de responsabilité.",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 1580, text="En aucun cas l’auteur / vendeur du logiciel ne sera responsable de dommage corporel, ni de quelconque dommage accidentel, spécial, indirect ou accessoire, y compris de façon non limitative, les dommages dus aux pertes de bénéfices",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1600, text=", pertes de données, produit, interruption des affaires, la perte d'information commerciale ou toute autre perte pécuniaire résultant de l'utilisation ou de l'impossibilité d'utilisation de ce ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1620, text="en aucun cas être responsable de tout problème survenant sur l'ordinateur utilisant Dariush-Shadi, et ceci, que le logiciel soit ou non, directement ou indirectement lié. quelle qu’en soit la cause. De plus, l’auteur ne peut",anchor="w", font="Arial 8", fill="black")

    canvas3.create_text(10, 1650, text="8. Accord complet.",anchor="w", font="Arial 12 bold", fill="black")
    canvas3.create_text(10, 1670, text="Cette licence constitue l’intégralité de l’accord entre les parties quant à l’utilisation du logiciel objet de la présente licence, et remplace toutes les propositions ou accords antérieurs ou actuels, écrits ou verbaux, à ce sujet.",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1690, text="Aucun amendement ni aucune modification de cette licence ne prendront effet à moins d’être stipulés par écrit et signés par un représentant dûment agréé de l’auteur. Toute traduction de la présente licence est effectuée pour des besoins locaux.",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1710, text="En cas de litige entre la version française et toute autre version, seule la version française sera d’application. Le non-respect de ces directives d'utilisation entraînera l'annulation de la, ou des licences ",anchor="w", font="Arial 8", fill="black")
    canvas3.create_text(10, 1730, text="et fera l'objet d'un dépôt de plainte. Les contrevenants s'exposent à de sévères sanctions civiles et/ou pénales et seront poursuivis jusqu'aux peines maximales prévues par la loi.",anchor="w", font="Arial 8", fill="black")


    canvas3.focus_set()


    defilY.grid( row=0, column=1, sticky=Tki.N+Tki.S )
    canvas3.grid(row=0, column=0)


def apropos():
     global Version
     showinfo("à propos","Dariush-Shadi version  " +Version + '\n' +'\n'+"2019 "+ 'Programme Python'+ '\n'+'\n' +"Freeware (voir licence pour les conditions d'utilisation)"+ '\n'+'\n' +"Auteur : Frédéric Boissac"+ '\n'+'\n'+'Site : http://fred.boissac.free.fr/index.htm'+'\n'+'\n'+"Contact : prof.boissac@gmail.com")






if __name__ == '__main__':


    # Création de la fenêtre principale
    Mafenetre = Tki.Tk()
    Version="1.3"
    Mafenetre.title("Dariush-Shadi Version " +Version+" 2019 Freeware Boissac Frédéric")
    Mafenetre.geometry('650x750')

    #variables globales
    photoplateau=Tki.PhotoImage(file="images/petitplateau.png")
    PionNoir=Tki.PhotoImage(file="images/PionNoirEnBuy.png")
    PionBlanc=Tki.PhotoImage(file="images/PionBlancEnBuy.png")
    SUIVANT=Tki.PhotoImage(file="images/suivant.png")
    RETOUR=Tki.PhotoImage(file="images/avant.png")

    if pygame_active : mixer.init()
    DesactiveSon = Tki.IntVar ()
    DesactiveSon.set(1)
    if pygame_active : son = mixer.Sound("images/coupjoue.wav") # importe un son

    selection=[0,0,0,0] # coordonnées de la case cliquée et du dernier coup joué [xclic,yclic,xdernier,ydernier]
    SynchroAffiche=False
    NbreMoteursDariush=2
    Dariush_MTC_Nbre_Simulations,Dariush_UCT_Nbre_Simulations=10000,10000
    Canevas = Tki.Canvas(Mafenetre,width=650,height=800,cursor="hand2",background='#e6e6ff')

    En_cours_De_Partie=True
    #Les objets
    LePlateau=Utils.class_plateau.Plateau()
    LePlateauMoteur=Utils.class_plateau.Plateau() #copie de l'objet LePlateau transmise aux moteurs
    Les_coups_joues=[]
    for i in range(100) : Les_coups_joues.append((0,0,0,0))
    Num_Du_Coup=0

    GMJ=Gestion_Moteurs_Joueurs()
    Thread_EM=Ecoute_Moteur()
    Thread_EM.start()

    Thread_Chrono=Chrono()
    Thread_Chrono.start()


    #affichage initial
    affiche()


    #menu
    menu_barre_den_haut = Tki.Menu(Mafenetre,font="Arial 10 bold",foreground='red',selectcolor='blue')  ## Barre de menu
    Mafenetre['menu']=menu_barre_den_haut
    menu_barre_den_haut.configure(font="Arial 10 bold",foreground='red',selectcolor='blue')
    menu_barre_den_haut.configure(bg="red")

    menufichier = Tki.Menu(menu_barre_den_haut, tearoff = 0)  ## Menu fils menuExample (tearoff=1 menu  detachable)
    menufichier.add_command(label="Ouvrir", command=ouvreunfichier)  ## Ajout d'une option au menu fils menuFile
    menufichier.add_separator() ## Ajout d'une ligne séparatrice
    menufichier.add_command(label="Enregistrer", command=enregistrefichier)
    menufichier.add_separator() ## Ajout d'une ligne séparatrice
    menufichier.add_command(label="Nouvelle partie", command=initialise)
    menufichier.add_separator() ## Ajout d'une ligne séparatrice
    menufichier.add_command(label="Quitter", command=Mafenetre.destroy)

    menumoteurs = Tki.Menu(menu_barre_den_haut,selectcolor='red',tearoff = 0) ## Menu Fils
    menumoteurs.add_command(label="Importer un nouveau moteur",command = GMJ.ImporteMoteur)
    menumoteurs.add_separator() ## Ajout d'une ligne séparatrice

    sous_menu_liste_moteurs = Tki.Menu(menumoteurs,font="Arial 10 bold", tearoff=0)
    menumoteurs.add_cascade(label='Supprimer un moteur', menu=sous_menu_liste_moteurs)

    menumoteurs.add_separator() ## Ajout d'une ligne séparatrice
    sous_menu_Parametres_moteurs_Dariush = Tki.Menu(menumoteurs,font="Arial 10 bold", tearoff=0)
    menumoteurs.add_cascade(label='Paramètres des moteurs Dariush', menu=sous_menu_Parametres_moteurs_Dariush)
    sous_menu_Parametres_moteurs_Dariush.add_command(label="Réglage : Dariush-Monte-Carlo",command=lambda choix=1:GMJ.ModificationMoteurDariush(choix))
    sous_menu_Parametres_moteurs_Dariush.add_command(label="Réglage : Dariush-UCT",command=lambda choix=2:GMJ.ModificationMoteurDariush(choix))
    sous_menu_Parametres_moteurs_Dariush.add_radiobutton(label="Activer tous les coeurs du microprocesseur",value=1,variable=GMJ.Multi_Process,command=lambda choix=3:GMJ.ModificationMoteurDariush(choix))
    menumoteurs.add_separator() ## Ajout d'une ligne séparatrice

    menumoteurs.add_command(label="Tournoi automatique", command=GMJ.TournoiAuto)

    menujoueurs = Tki.Menu(menu_barre_den_haut, tearoff = 0) ## Menu Fils
    sous_menu_liste_joueurblanc = Tki.Menu(menujoueurs,font="Arial 10 bold", tearoff=0)
    menujoueurs.add_cascade(label='Joueur Blanc', menu=sous_menu_liste_joueurblanc)

    menujoueurs.add_separator() ## Ajout d'une ligne séparatrice
    sous_menu_liste_joueurnoir = Tki.Menu(menujoueurs,font="Arial 10 bold", tearoff=0)
    menujoueurs.add_cascade(label='Joueur Noir', menu=sous_menu_liste_joueurnoir)

    GMJ.Affiche_sous_menus_moteurs()



    menuoutils = Tki.Menu(menu_barre_den_haut, tearoff = 0)  ## Menu fils menuExample (tearoff=1 menu  detachable)

    menuoutils.add_checkbutton(label="Désactiver le son",variable= DesactiveSon , onvalue = 1, offvalue = 0)



    menuHelp = Tki.Menu(menu_barre_den_haut, tearoff = 0) ## Menu Fils
    menuHelp.add_command(label="Règle/Renseignements", command=affiche_aide)
    menuHelp.add_separator() ## Ajout d'une ligne séparatrice
    menuHelp.add_command(label="Licence", command=affiche_licence)
    menuHelp.add_separator() ## Ajout d'une ligne séparatrice
    menuHelp.add_command(label="À propos", command=apropos)

    menu_barre_den_haut.add_cascade(label = "Fichiers", menu=menufichier)
    menu_barre_den_haut.add_cascade(label = "Moteurs", menu=menumoteurs)
    menu_barre_den_haut.add_cascade(label = "Joueurs", menu=menujoueurs)
    menu_barre_den_haut.add_cascade(label = "Outils", menu=menuoutils)
    menu_barre_den_haut.add_cascade(label = "Aide", menu=menuHelp)
    #fin du menu



    Canevas.bind('<Button-1>', Clic)

    Canevas.grid(row=2, column=0)

    Canevas.mainloop()

    En_cours_De_Partie=False
    print('Fin de partie')
   # Thread_EM.join()
   # Thread_Chrono.join()#fermer les threads
