#Import des librairies
import json
from random import *
import random
import os
from time import sleep

#Récupération de la Configuration dans le fichier config-app.json
ConfigApp = open('config-app.json')
ConfigAppData = json.load(ConfigApp)

AppWidth = ConfigAppData['WidthApplication']
AppHeight = ConfigAppData['HeightApplication']
AppName = ConfigAppData['NameApplication']

#Vérification si Pygame est bien installé sur l'ordinateur du joueur
try:
    import pygame
    from pygame import *
except:
    print('\n\nPygame n\'est pas installé sur votre appareil !\nL\'installation va commencer dans 5 secondes.\n\n')
    sleep(5)
    os.system('pip install -U pygame')

import pygame, sys
from bouton import Bouton

#Configuration de Pygame
pygame.init ()
clock = pygame.time.Clock()

#Choix de la taille de l'interface
SCREEN = pygame.display.set_mode((AppWidth, AppHeight))
#Choix du nom de l'inteface
pygame.display.set_caption(AppName)

#Importantion des images (icon, background, etc.)
BG = pygame.image.load("assets/Background.png")
ICON = pygame.image.load("assets/icon.jpg")
RED_HEART = pygame.image.load("assets/RedHeart.png")
widthImg = RED_HEART.get_rect().width
heightImg = RED_HEART.get_rect().height
RED_HEART = pygame.transform.scale(RED_HEART, (widthImg/6,heightImg/6))
BLACK_HEART = pygame.image.load("assets/BlackHeart.png")
widthImg = BLACK_HEART.get_rect().width
heightImg = BLACK_HEART.get_rect().height
BLACK_HEART = pygame.transform.scale(BLACK_HEART, (widthImg/6,heightImg/6))

#Choix de l'icon du jeu
pygame.display.set_icon(ICON)

#Paramètre de la Police et de sa taille
def get_font(taille):
    return pygame.font.Font("assets/font.ttf", taille)

#Page de choix des actions
def play(score, vie, came_from_home):
    while True:
        #Position de la souris sur l'écran
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        #Image en arrière plan
        SCREEN.blit(BG, (0, 0))

        #Titre de la page
        PLAY_TEXT = get_font(40).render("Choississez votre Action:", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        #Bouton des actions
        PIERRE_BUTTON = Bouton(image=None, pos=(AppWidth/2, 250), 
                            text_input="PIERRE", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")
        FEUILLE_BUTTON = Bouton(image=None, pos=(AppWidth/2, 325), 
                            text_input="FEUILLE", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")
        CISEAUX_BUTTON = Bouton(image=None, pos=(AppWidth/2, 400), 
                            text_input="CISEAUX", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")
        LEZARD_BUTTON = Bouton(image=None, pos=(AppWidth/2, 475), 
                            text_input="LEZARD", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")
        SPOCK_BUTTON = Bouton(image=None, pos=(AppWidth/2, 550), 
                            text_input="SPOCK", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")

        #Vérifie sur le joueurs viens de la page d'acceuil ou s'il vient de la page de combat.
        if came_from_home == True:
            #Affiche le bouton retour
            RETOUR = Bouton(image=None, pos=(180, AppHeight-50), 
                text_input="RETOUR", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")
            RETOUR.changeColor(PLAY_MOUSE_POS)
            RETOUR.update(SCREEN)
            score = 0
            vie = 3
        if came_from_home == False:
            #Affiche la vie et le score
            SCORE_TEXT = get_font(40).render("Score:"+str(score), True, "White")
            SCORE_RECT = SCORE_TEXT.get_rect(center=(AppWidth-200, AppHeight-40))
            SCREEN.blit(SCORE_TEXT, SCORE_RECT)
            if vie == 3:
                SCREEN.blit(RED_HEART, (15,AppHeight-75))
                SCREEN.blit(RED_HEART, (85,AppHeight-75))
                SCREEN.blit(RED_HEART, (155,AppHeight-75))
            elif vie == 2:
                SCREEN.blit(RED_HEART, (15,AppHeight-75))
                SCREEN.blit(RED_HEART, (85,AppHeight-75))
                SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
            elif vie == 1:
                SCREEN.blit(RED_HEART, (15,AppHeight-75))
                SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
                SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
            else:
                SCREEN.blit(BLACK_HEART, (15,AppHeight-75))
                SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
                SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
                
        #Ajoute les boutons sur l'écran
        for button in [PIERRE_BUTTON, FEUILLE_BUTTON, CISEAUX_BUTTON, LEZARD_BUTTON, SPOCK_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)
        
        #Vérifie si les boutons sont cliqué
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PIERRE_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    combat(score, vie, "Pierre")
                if FEUILLE_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    combat(score, vie, "Feuille")
                if CISEAUX_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    combat(score, vie, "Ciseaux")
                if LEZARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    combat(score, vie, "Lezard")
                if SPOCK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    combat(score, vie, "Spock")
                if came_from_home==True:
                    if RETOUR.checkForInput(PLAY_MOUSE_POS):
                        main_menu()


        pygame.display.update()

#Page de Combat
def combat(score, vie, action):

    #Génération du choix de l'ordinateur
    game_choice = ["Pierre","Feuille","Ciseaux","Lezard","Spock"]
    random_i = random.randint(0, 4)
    bot_choice = game_choice[random_i]

    #Page de combat avec animation d'affichage du choix du joueur
    x = -1000
    while x < AppWidth/4:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        COMBAT_TEXT = get_font(40).render("Combat Epique !!", True, "Yellow")
        COMBAT_RECT = COMBAT_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(COMBAT_TEXT, COMBAT_RECT)

        VS_TEXT = get_font(100).render("VS", True, "Red")
        VS_RECT = VS_TEXT.get_rect(center=(AppWidth/2, AppHeight/2))
        SCREEN.blit(VS_TEXT, VS_RECT)
        
        YOU_TEXT = get_font(40).render("Vous", True, "White")
        YOU_RECT = YOU_TEXT.get_rect(center=(AppWidth/4, AppHeight/2-120))
        SCREEN.blit(YOU_TEXT, YOU_RECT)

        BOT_TEXT = get_font(40).render("Bot", True, "White")
        BOT_RECT = BOT_TEXT.get_rect(center=(AppWidth/4+AppWidth/2, AppHeight/2-120))
        SCREEN.blit(BOT_TEXT, BOT_RECT)

        SCORE_TEXT = get_font(40).render("Score:"+str(score), True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(AppWidth-200, AppHeight-40))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        if vie == 3:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(RED_HEART, (85,AppHeight-75))
            SCREEN.blit(RED_HEART, (155,AppHeight-75))
        elif vie == 2:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(RED_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
        elif vie == 1:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
        else:
            SCREEN.blit(BLACK_HEART, (15,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))

        ACTION_JOUEUR_TEXT = get_font(40).render(str(action), True, "#9C6CFF")
        ACTION_JOUEUR_RECT = ACTION_JOUEUR_TEXT.get_rect(center=(x, AppHeight/2))
        SCREEN.blit(ACTION_JOUEUR_TEXT, ACTION_JOUEUR_RECT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        x = x + 10

    #Page de combat avec animation d'affichage du choix de l'ordinateur
    x = AppWidth+1000
    while x > AppWidth/4+AppWidth/2:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        COMBAT_TEXT = get_font(40).render("Combat Epique !!", True, "Yellow")
        COMBAT_RECT = COMBAT_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(COMBAT_TEXT, COMBAT_RECT)

        VS_TEXT = get_font(100).render("VS", True, "Red")
        VS_RECT = VS_TEXT.get_rect(center=(AppWidth/2, AppHeight/2))
        SCREEN.blit(VS_TEXT, VS_RECT)
        
        YOU_TEXT = get_font(40).render("Vous", True, "White")
        YOU_RECT = YOU_TEXT.get_rect(center=(AppWidth/4, AppHeight/2-120))
        SCREEN.blit(YOU_TEXT, YOU_RECT)

        BOT_TEXT = get_font(40).render("Bot", True, "White")
        BOT_RECT = BOT_TEXT.get_rect(center=(AppWidth/4+AppWidth/2, AppHeight/2-120))
        SCREEN.blit(BOT_TEXT, BOT_RECT)

        SCORE_TEXT = get_font(40).render("Score:"+str(score), True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(AppWidth-200, AppHeight-40))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        if vie == 3:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(RED_HEART, (85,AppHeight-75))
            SCREEN.blit(RED_HEART, (155,AppHeight-75))
        elif vie == 2:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(RED_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
        elif vie == 1:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
        else:
            SCREEN.blit(BLACK_HEART, (15,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))

        ACTION_JOUEUR_TEXT = get_font(40).render(str(action), True, "#9C6CFF")
        ACTION_JOUEUR_RECT = ACTION_JOUEUR_TEXT.get_rect(center=(AppWidth/4, AppHeight/2))
        SCREEN.blit(ACTION_JOUEUR_TEXT, ACTION_JOUEUR_RECT)

        ACTION_ORDI_TEXT = get_font(40).render(bot_choice, True, "#9C6CFF")
        ACTION_ORDI_RECT = ACTION_ORDI_TEXT.get_rect(center=(x, AppHeight/2))
        SCREEN.blit(ACTION_ORDI_TEXT, ACTION_ORDI_RECT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        x = x - 10

    i = 1000
    while i > 0:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        COMBAT_TEXT = get_font(40).render("Combat Epique !!", True, "Yellow")
        COMBAT_RECT = COMBAT_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(COMBAT_TEXT, COMBAT_RECT)

        VS_TEXT = get_font(100).render("VS", True, "Red")
        VS_RECT = VS_TEXT.get_rect(center=(AppWidth/2, AppHeight/2))
        SCREEN.blit(VS_TEXT, VS_RECT)
        
        YOU_TEXT = get_font(40).render("Vous", True, "White")
        YOU_RECT = YOU_TEXT.get_rect(center=(AppWidth/4, AppHeight/2-120))
        SCREEN.blit(YOU_TEXT, YOU_RECT)

        BOT_TEXT = get_font(40).render("Bot", True, "White")
        BOT_RECT = BOT_TEXT.get_rect(center=(AppWidth/4+AppWidth/2, AppHeight/2-120))
        SCREEN.blit(BOT_TEXT, BOT_RECT)

        SCORE_TEXT = get_font(40).render("Score:"+str(score), True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(AppWidth-200, AppHeight-40))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        if vie == 3:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(RED_HEART, (85,AppHeight-75))
            SCREEN.blit(RED_HEART, (155,AppHeight-75))
        elif vie == 2:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(RED_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
        elif vie == 1:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
        else:
            SCREEN.blit(BLACK_HEART, (15,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))

        ACTION_JOUEUR_TEXT = get_font(40).render(str(action), True, "#9C6CFF")
        ACTION_JOUEUR_RECT = ACTION_JOUEUR_TEXT.get_rect(center=(AppWidth/4, AppHeight/2))
        SCREEN.blit(ACTION_JOUEUR_TEXT, ACTION_JOUEUR_RECT)

        ACTION_ORDI_TEXT = get_font(40).render(bot_choice, True, "#9C6CFF")
        ACTION_ORDI_RECT = ACTION_ORDI_TEXT.get_rect(center=(AppWidth/4+AppWidth/2, AppHeight/2))
        SCREEN.blit(ACTION_ORDI_TEXT, ACTION_ORDI_RECT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        i = i - 7

    #Vérifie si le joueur gagne ou perd le combat et prépare l'affichage
    vie_joueur = ""
    score_joueur = ""
    title = ""
    desc = ""
    color = ""
    def GagneOuPerd(Ordinateur, Joueur):
        #Vérifie si le joueur gagne.
        if Joueur == "Feuille" and Ordinateur == "Pierre":
            return "Victoire"
        elif Joueur == "Feuille" and Ordinateur == "Spock" :
            return "Victoire"
        elif Joueur == "Ciseaux" and Ordinateur == "Feuille" :
            return "Victoire"
        elif Joueur == "Ciseaux" and Ordinateur == "Lezard" :
            return "Victoire"
        elif Joueur == "Pierre" and Ordinateur == "Ciseaux" :
            return "Victoire"
        elif Joueur == "Pierre" and Ordinateur == "Lezard" :
            return "Victoire"
        elif Joueur == "Lezard" and Ordinateur == "Spock" :
            return "Victoire"
        elif Joueur == "Lezard" and Ordinateur == "Feuille" :
            return "Victoire"
        elif Joueur == "Spock" and Ordinateur == "Ciseaux" :
            return "Victoire"
        elif Joueur == "Spock" and Ordinateur == "Pierre" :
            return "Victoire"
        #Vérifie si il y a match nul.
        elif Joueur == Ordinateur :
            return "Match Nul"
        #Vérifie si le joueur perd.
        else:
            return "Défaite"
    
    #Préparation de l'affichage en cas de Victoire
    if GagneOuPerd(bot_choice,action) == "Victoire":
        vie_joueur = vie
        score_joueur = score + 2
        title = "Bien Joué !"
        desc = "Vous avez gagné 2 points !"
        color = "Yellow"
    #Préparation de l'affichage en cas de Match Nul
    elif GagneOuPerd(bot_choice,action) == "Match Nul":
        vie_joueur = vie
        score_joueur = score + 1
        title = "Match Nul"
        desc = "Vous avez gagné 1 points !"
        color = "Pink"
    #Préparation de l'affichage en cas de Défaite
    elif GagneOuPerd(bot_choice,action) == "Défaite":
        vie_joueur = vie - 1
        score_joueur = score
        title = "Mince !"
        desc = "Vous avez perdu 1 vie !"
        color = "Red"

    #Vérifie si le joueur à encore des vies
    if(vie_joueur == 0):
        defaite(score_joueur)
    
    #Page de combat avec l'affichage des résultat (Victoire, Match Nul, Défaite)
    while True:

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        RESULT_TEXT = get_font(100).render(title, True, color)
        RESULT_RECT = RESULT_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(RESULT_TEXT, RESULT_RECT)

        INFO_TEXT = get_font(30).render(desc, True, "White")
        INFO_RECT = INFO_TEXT.get_rect(center=(AppWidth/2, AppHeight/2))
        SCREEN.blit(INFO_TEXT, INFO_RECT)

        SCORE_TEXT = get_font(40).render("Score:"+str(score_joueur), True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(AppWidth-200, AppHeight-40))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        if vie_joueur == 3:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(RED_HEART, (85,AppHeight-75))
            SCREEN.blit(RED_HEART, (155,AppHeight-75))
        elif vie_joueur == 2:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(RED_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
        elif vie_joueur == 1:
            SCREEN.blit(RED_HEART, (15,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))
        else:
            SCREEN.blit(BLACK_HEART, (15,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (85,AppHeight-75))
            SCREEN.blit(BLACK_HEART, (155,AppHeight-75))

        CONTINUER_BUTTON = Bouton(image=None, pos=(AppWidth/2, AppHeight-120), 
            text_input="CONTINUER LA PARTIE", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")
        for button in [CONTINUER_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUER_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    play(score_joueur,vie_joueur,False)


        pygame.display.update()

#Page de défaite, apparait quand le joueur n'a plus de vie
def defaite(score):

    #Récupére les Meilleurs Scores
    TopPlayers = open('top-players.json')
    TopPlayersData = json.load(TopPlayers)
    Premier = TopPlayersData['1']
    Deuxième = TopPlayersData['2']
    Troisième = TopPlayersData['3']
    
    #Vérfie si l'utlisateur a battu le record ou si il prend la deuxième ou troisième place.
    if(score > Troisième):
        new_json = {"1":Premier, "2":Deuxième, "3": Troisième}
        if(score > Deuxième):
            if(score > Premier):
                new_json = {"1":int(score), "2":Premier, "3": Deuxième}
            else:
                new_json = {"1":Premier, "2":int(score), "3": Deuxième}
        else:
            new_json = {"1":Premier,"2":Deuxième, "3": int(score)}

        #Met a jour les meilleurs records dans le fichier top-players.json
        json_value = json.dumps(new_json)
        TopPlayers_edit = open('top-players.json', 'w')
        TopPlayers_edit.write(json_value)
        TopPlayers_edit.close()
    TopPlayers.close()

    #Affiche le score du joueur à la fin de la partie (lorsqu'il n'a plus de vie)
    while True:
        DEFAITE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        DEFAITE_TEXT = get_font(45).render("Echec !", True, "Red")
        DEFAITE_RECT = DEFAITE_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(DEFAITE_TEXT, DEFAITE_RECT)

        SCORE_TEXT = get_font(30).render("Vous avez malheureusement perdu !", True, "Red")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(640, AppHeight/2-25))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        SCORE_TEXT = get_font(30).render("Votre score est de "+str(score)+" points !", True, "Red")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(640, AppHeight/2+25))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        DEFAITE_BACK = Bouton(image=None, pos=(640, AppHeight-100), 
            text_input="REJOUER", font=get_font(75), base_color="#AFB5FF", hovering_color="#3D4EFF")

        DEFAITE_BACK.changeColor(DEFAITE_MOUSE_POS)
        DEFAITE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if DEFAITE_BACK.checkForInput(DEFAITE_MOUSE_POS):
                    main_menu()

        pygame.display.update()

#Page des Meilleurs Scores
def best_scores():
    while True:
        BEST_SCORES_MOUSE_POS = pygame.mouse.get_pos()

        #Récupére les Meilleurs Scores
        TopPlayers = open('top-players.json')
        TopPlayersData = json.load(TopPlayers)
        Premier = TopPlayersData['1']
        Deuxième = TopPlayersData['2']
        Troisième = TopPlayersData['3']

        SCREEN.blit(BG, (0, 0))

        #Affiche les meilleurs scores
        BEST_SCORES_TEXT = get_font(60).render("Meilleurs Scores", True, "White")
        BEST_SCORES_RECT = BEST_SCORES_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(BEST_SCORES_TEXT, BEST_SCORES_RECT)

        RECORD_1 = get_font(40).render("1) "+str(Premier), True, "Gold")
        RECORD_1_RECT = RECORD_1.get_rect(center=(AppWidth/2, AppHeight/2-100))
        SCREEN.blit(RECORD_1, RECORD_1_RECT)

        RECORD_2 = get_font(40).render("2) "+str(Deuxième), True, "Silver")
        RECORD_2_RECT = RECORD_2.get_rect(center=(AppWidth/2, AppHeight/2))
        SCREEN.blit(RECORD_2, RECORD_2_RECT)

        RECORD_3 = get_font(40).render("3) "+str(Troisième), True, "brown")
        RECORD_3_RECT = RECORD_3.get_rect(center=(AppWidth/2, AppHeight/2+100))
        SCREEN.blit(RECORD_3, RECORD_3_RECT)

        BEST_SCORES_BACK = Bouton(image=None, pos=(180, AppHeight-50), 
            text_input="Retour", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")

        BEST_SCORES_BACK.changeColor(BEST_SCORES_MOUSE_POS)
        BEST_SCORES_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BEST_SCORES_BACK.checkForInput(BEST_SCORES_MOUSE_POS):
                    main_menu()

        pygame.display.update()

#Page d'aide pour comprendre comment jouer
def aide():
    while True:
        AIDE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        #Affiche les meilleurs scores
        BEST_SCORES_TEXT = get_font(60).render("Comment Jouer ?", True, "GOLD")
        BEST_SCORES_RECT = BEST_SCORES_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(BEST_SCORES_TEXT, BEST_SCORES_RECT)

        AIDE_TEXT = get_font(20).render("Vous pouvez commencer une partie en cliquant sur Jouer.", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2-170))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("Après avoir commencé la partie, vous devez cliquer sur", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2-120))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("une des 5 actions pour commencer le premier combat.", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2-80))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("Une animation s'affiche ensuite, elle vous dévoile si vous", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2-30))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("avez gagné ou perdu votre match. Vous avez 3 vies, à chaque", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2+10))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("combat perdu vous perdez une vie (celle-ci sont visibles en", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2+50))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("bas à gauche de l'écran pendant une partie). Si vous perdez", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2+90))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("toutes vos vies, la partie s'arrète et votre score est", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2+130))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("affiché. Les meilleurs scores sont affichés dans la page", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2+170))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("des records. Si vous gagnez le combat, vous gagnez 2 points", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2+210))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("et si il y a Match Nul, vous gagnez 1 points. Bon jeu !", True, "White")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2, AppHeight/2+250))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("1 points", True, "#F3F781")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2+250, AppHeight/2+250))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("2 points", True, "#F3F781")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2+510, AppHeight/2+210))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("3 vies", True, "#F3F781")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2+330, AppHeight/2+10))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("Jouer", True, "#F3F781")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2+480, AppHeight/2-170))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)
        AIDE_TEXT = get_font(20).render("5 actions", True, "#F3F781")
        AIDE_RECT = AIDE_TEXT.get_rect(center=(AppWidth/2-260, AppHeight/2-80))
        SCREEN.blit(AIDE_TEXT, AIDE_RECT)

        AIDE_BACK = Bouton(image=None, pos=(180, AppHeight-50), 
            text_input="Retour", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")

        AIDE_BACK.changeColor(AIDE_MOUSE_POS)
        AIDE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AIDE_BACK.checkForInput(AIDE_MOUSE_POS):
                    main_menu()

        pygame.display.update()

#Page du menu principale avec les différents boutons.
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("PFCLS MENU", True, "#d98d00")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Bouton(image=None, pos=(640, 325), 
                            text_input="JOUER", font=get_font(90), base_color="#5662FF", hovering_color="#1F31FF")
        BEST_SCORES_BUTTON = Bouton(image=None, pos=(640, 450), 
                            text_input="RECORDS", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")
        AIDE_BUTTON = Bouton(image=None, pos=(640, 525), 
                            text_input="AIDE", font=get_font(45), base_color="#AFB5FF", hovering_color="#3D4EFF")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, BEST_SCORES_BUTTON, AIDE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(1,1,True)
                if BEST_SCORES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    best_scores()
                if AIDE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    aide()

        pygame.display.update()

#Page affiché au lancement du jeu (ici page d'accueil)
main_menu()