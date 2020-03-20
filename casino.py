# -*- coding: latin-1 -*-
from random import randint
from math import *
import sys
from datetime import datetime
import os

import numpy as np
import matplotlib.pyplot as plt
from inputimeout import inputimeout, TimeoutOccurred
                                              

def exitGame():

    if argent == 0:
        print("Vous n'avez plus d'argent , au revoir ! ")
        lecture(2)
        sys.exit(0)

    while True:
        try:
            decisionExitGame = inputimeout(prompt='Voulez-vous quitter le jeu ? (o/n) : ', timeout=10)
            decisionExitGame = decisionExitGame.upper()
        except TimeoutOccurred:
            print("10 secondes sont passees...Vous quittez le jeu automatiquement")
            lecture(2)
            sys.exit(0)

        if decisionExitGame != "O" and decisionExitGame != "N":
            print("Vous n'avez pas ecrit la bonne lettre\n")
        elif decisionExitGame == "N":
            return True
        elif decisionExitGame == "O":
            lecture(2)
            sys.exit(0)

            
def jeu(level):
    global argent
    global mise
    global gain

    gain = 0
    #nb_partie += 1

    #Determine le nombre aleatoire max et le nombre d'essai possible en fonction du niveau
    if level == 1:
        nb_max = 10
        nb_essai = 5
        mise_1 = 2
        mise_2 = 0.5

    elif level == 2:
        nb_max = 20
        nb_essai = 7
        mise_1 = 3
        mise_2 = 1

    elif level == 3:
        nb_max = 30
        nb_essai = 10
        mise_1 = 4
        mise_2 = 2

    nb_python  = randint(1, nb_max)

    #les essais de l'utilisateur
    nb_coup = 0
    nb_user = 0

    while nb_coup < nb_essai:
        try:
            nb_user = int(inputimeout(prompt="Niveau " + str(level) + ' | Essai numero '+ str(nb_coup + 1) +' Saisissez le nombre mystere :', timeout=5 ))
        except ValueError:
            print("Vous n'avez pas saisi de nombre")
            continue
        except TimeoutOccurred:
            print("Trop lent !!! 5 secondes sont passees...\n")
            nb_coup += 1
            if nb_coup < nb_essai:
                continue
            

        if(nb_user  == nb_python):
            print("Bravo, vous avez gagne ! Les statistiques de la partie sont les suivantes :\n")
            print("Vous avez reussi au bout du """+ str(nb_coup + 1) +"e coup")
            
            if nb_coup + 1 == 1:
                gain = ceil(mise*mise_1)
                argent = argent + gain
                print("Vous multipliez votre mise par"+ str(mise_1) +", vous gagnez " + str(gain)+" Euros ")
                print("Il vous reste " + str(argent)+" Euros")
                sauvegarde(level, nb_coup + 1)

            elif nb_coup + 1 == 2:
                gain = ceil(mise*mise_2)
                argent = argent + gain
                print("Vous multipliez votre mise par"+ str(mise_2) +", vous gagnez " + str(gain)+" Euros ")
                print("Il vous reste " + str(argent)+" Euros")
                sauvegarde(level, nb_coup + 1)

            else:    
                argent = argent - mise
                print("Vous perdez votre mise, vous perdez " + str(mise)+" Euros *")
                print("Il vous reste " + str(argent)+" Euros")
                sauvegarde(level, nb_coup + 1 )
                
            if argent == 0:
                exitGame()
            return True

        elif(nb_coup == nb_essai):
            argent = argent - mise
            print('Chiffre incorrect, Vous avez perdu ! Mon nombre est '+ str(nb_python) +' !\n')
            print("Vous perdez votre mise, vous perdez " + str(mise)+" Euros ")
            print("Il vous reste " + str(argent)+" Euros *")
            return False

        elif nb_user > nb_max:
             print('Votre nombre depasse la limite de ' + str(nb_max))
             continue
        elif nb_user < 0:
            print('Votre nombre est inferieur 0')
            continue
        elif nb_user > nb_python:
             print('Votre nombre est trop grand !')
        
        elif nb_user < nb_python:
             print('Votre nombre est trop petit !')
  
        
        print ("Il vous reste "+ str(nb_essai -1 - nb_coup)  +" chance !\n")
        nb_coup += 1

def sauvegarde(level, nb_coup):

    now = datetime.now()
    date1 = now.strftime("%d/%m/%Y %H:%M:%S")

    f = open('sauvegarde.txt',"a", encoding = 'utf-8')
    f.write('\n'+ name_user + ';' + date1 + ';' + str(level) + ';' + str(nb_coup) + ';' + str(argent) + ';' + str(mise) + ';' + str(gain))
    f.close()

def lecture(passage):
    first_date = ""
    nb_coup = 0
    nb_one = 0
    nb_enregist = 0
    mise_total = 0

    best_level = 0
    best_mise = 0
    best_gain = 0
    mise_moy = 0
    nb_coup_moy = 0
    the_List = list()
   
    list_Parties = []
    list_Mise = []
    list_Coups = []
    list_Gain = []
    list_Dotation = []

    try:
        with open('sauvegarde.txt', 'r') as f : 
            for ligne in f:
                
                the_List = ligne.split(";")
                nom = the_List[0]
                nom = nom.upper()

                if nom == name_user.upper():
                    #incremente nombre enregistrement
                    nb_enregist += 1

                    if first_date == "":
                        first_date = the_List[1]
                    #Determine le nombre de fois où le joueur a gagné du 1er coup
                    if  int(the_List[3]) == 1:
                        nb_one += 1
                    
                    #incremente total nombre de coups
                    nb_coup += int(the_List[3])
                    
                    #Determine le niveau le plus élevé que le joueur a atteint
                    the_level = the_List[2]
                    the_level = int(the_level)
                    if best_level == 0 or best_level < the_level:
                        best_level = the_level

                    #Determine la mise la plus élevé  du joueur
                    la_mise = the_List[5]
                    la_mise = int(la_mise)
                    if best_mise == 0 or best_mise < la_mise:
                        best_mise = la_mise

                    #incremente la mise total
                    mise_total += la_mise
                    
                    #Determine le gain le plus élevé  du joueur
                    le_gain = the_List[6]
                    le_gain = int(le_gain)
                    if best_gain == 0 or best_gain < le_gain:
                        best_gain = le_gain    

                    #ajout nombre de jeu
                    list_Parties.append(nb_enregist)
                    #ajout mise par jeu
                    list_Mise.append(la_mise)
                    #ajout nombre de coup 
                    list_Coups.append(int(the_List[3]))
                    #ajout gain par jeu
                    list_Gain.append(int(the_List[6]))
                    #ajout dotation par jeu
                    list_Dotation.append(int(the_List[4]))

        #calcul moyenne
        if nb_coup != 0:
            nb_coup_moy = ceil(nb_coup / nb_enregist)
           
        if mise_total != 0:
            mise_moy = ceil(mise_total / nb_enregist)
           

    except IOError:
        return
           
    if first_date != "" and passage != 2:

        print("\nRebonjour "+ name_user +", Content de vous revoir au Casino, pret pour un nouveau challenge ?")
        print(" Voici les statistiques, depuis la 1ere fois : "+ first_date)
        print("\n   Vos meilleures statistiques : \n")
        print("     Le niveau atteint le plus eleve : "+ str(best_level) +"\n")
        print("     Vous avez reussi a trouver le bon nombre des le 1er coup "+ str(nb_one) +" fois\n")
        print("     Le gain le plus eleve est de : "+ str(best_gain) +" Euros\n")
        print("     La mise la plus elevee est de : "+ str(best_mise) +" Euros\n")

        print("\n   Vos moyennes : \n")
        print("     La mise moyenne est de  : "+ str(mise_moy) + " Euros\n")
        print("     Le nombre moyen de tentatives pour trouver le bon nombre est : "+ str(nb_coup_moy) +" fois\n")
        print("\n   Pouvez-vous faire mieux ? \n")
    elif passage == 2:

        #graphiqueSolde(list_Parties,list_Gain,"Parties","Euros","Dotation en Euros par Parties","Dotation en Euros")
        graphiqueSolde(list_Parties,list_Mise,"Parties","Euros","Mise en Euros par partie","Mise en Euros")
        graphiqueSolde(list_Parties,list_Coups,"Parties","Nombre de coups","Nombre de coups par Parties","Nombre de coups")
        graphiqueSolde(list_Parties,list_Gain,"Parties","Euros","Gain en Euros par Parties","Gain en Euros")
    

def miser_argent():
    global argent
    global mise

    mise = 0

    while mise <= 0 or mise > argent:
            mise = input("Entrez une mise inferieure ou egale a "+ str(argent) + " Euros : ")
            # On convertit la mise
            try:
                mise = int(mise)
            except ValueError:
                print("Vous n'avez pas saisi de nombre entier")
                mise = -1
                continue
            if mise <= 0:
                print("La mise saisie est negative ou nulle.")
            if mise > argent:
                print("Vous ne pouvez pas miser autant, vous n'avez que", argent, "Euros")

def affichage_regle(niveau):
    
    if niveau == 1:
        print("Vous  etes Level 1.\n")
        print("Rappelez vous, le principe est le meme sauf que mon nombre est entre 1 et 10 !")
        print("Et que le gain si vous gagnez du premier coup equivaut a la mise x 2 !")
        print("Et que le gain si vous gagnez du deuxieme coup equivaut a la mise / 2 !\n")
        print("A partir du troisieme coup vous perdez votre mise !\n")
    elif niveau == 2:
        print("Super ! Vous passez au Level 2.\n\n")
        print("Rappelez vous, le principe est le meme sauf que mon nombre est maintenant entre 1 et 20 !")
        print("Et que le gain si vous gagnez du premier coup equivaut a la mise x 3 !")
        print("Et que le gain si vous gagnez du deuxieme coup equivaut a la mise !\n")
        print("A partir du troisieme coup vous perdez votre mise !\n")
    elif niveau == 3:
        print("Super ! Vous passez au Level 3.\n\n")
        print("Rappelez vous, le principe est le meme sauf que mon nombre est maintenant entre 1 et 30 !\n")
        print("Et que le gain si vous gagnez du premier coup equivaut a la mise x 4 !")
        print("Et que le gain si vous gagnez du deuxieme coup equivaut a la mise x 2 !\n")
        print("A partir du troisieme coup vous perdez votre mise !\n")

def graphiqueSolde(donneesX,donneesY,enteteX,enteteY,Titre,LabelY):

    #calcul moyenne donnees en absicce
    moyenne = 0
    listMoy = []

    for elem in donneesY:   
        moyenne += elem
    moyenne = moyenne / len(donneesY)

    for elem in donneesY:
        listMoy.append(moyenne)
        
    #Paramètre et affichage graphique
    plt.plot(np.array(donneesX), np.array(donneesY), label=LabelY)
    plt.plot(np.array(donneesX),  np.array(listMoy), label="Moyenne " + LabelY)
    plt.legend()
    plt.xlabel(enteteX)
    plt.ylabel(enteteY)
    plt.title(Titre + " de " + name_user.upper())
    plt.show() # affiche la figure a l'ecran

global date1
global date2
global nb_partie
global dotation
global name_user

name_user = input('Je suis Python. Quel est votre pseudo ? : ')
lecture(1)

nb_partie=0
mise=0
argent=0
dotation = argent

#argent
while argent <= 0:
    try:
        argent = int(input("Combien d'argent avez vous a jouer ? : "))
    except ValueError:
        print("Vous n'avez pas saisi de nombre entier")
        continue
    if argent <= 0:
        print("L'argent' saisie est negative ou nulle.")


while True:

    miser_argent()
    affichage_regle(1)

    if jeu(1) != False:

        affichage_regle(2)
        exitGame()
        miser_argent()

        while True:
            if jeu(2) != False:

                affichage_regle(3)
                exitGame()
                miser_argent()

                while True:
                    if jeu(3) != False:
                        print("\nBravo "+ name_user +" votre solde est de "+ str(argent) + " Euros !! A la prochaine !\n\n")
                        sys.exit(0)
                    else:
                        exitGame()
                        miser_argent()
                        
            else:
                exitGame()
                miser_argent()
    else:
        exitGame()
        miser_argent()


