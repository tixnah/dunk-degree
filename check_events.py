# check_events.py
# Gère les événements du menu, les interactions de l'utilisateur en dehors du gameplay direct, l'affichage des différents écrans du menu (principal, guide, paramètres), et la sélection de l'avatar et du ballon.
# Gère également les événements de base du jeu (QUIT, entrées clavier pour le ballon).

import pygame
# Importation des fonctions de `trajectory` pour les actions du ballon et de `sound_manager` pour la musique.
from trajectory import *
import sound_manager

# --- Chargement initial des images ---

# Fonds d'écran
menu_bg_raw = pygame.image.load("image/menu.png")  # Menu principale
guide_bg_raw = pygame.image.load("image/guide.png")  # Le guide
game_bg_raw = pygame.image.load("image/background.png")  # Fond du jeu
parameter_on_bg_raw = pygame.image.load("image/parameter_on.png")  # Fond des paramètres (musique ON)
parameter_off_bg_raw = pygame.image.load("image/parameter_off.png")  # Fond des paramètres (musique OFF)

# Images des ballons pour la sélection dans les paramètres
violet_ball_img_raw = pygame.image.load("image_menu/violet_ball.png") # Balle violette
blue_ball_img_raw = pygame.image.load("image_menu/blue_ball.png") # Balle bleu
orange_ball_img_raw = pygame.image.load("image_menu/orange_ball.png") # Balle orange
selected_violet_ball_img_raw = pygame.image.load("image_menu/selected_violet_ball.png") # Balle violette selectionnée
selected_blue_ball_img_raw = pygame.image.load("image_menu/selected_blue_ball.png") # Balle bleu selectionnée
selected_orange_ball_img_raw = pygame.image.load("image_menu/selected_orange_ball.png") # Balle orange selectionnée

# Images des avatars pour la sélection dans les paramètres
avatar_1_img_raw = pygame.image.load("image_menu/avatar_1.png")  # Avatar 1 (cheveux noir)
avatar_2_img_raw = pygame.image.load("image_menu/avatar_2.png")  # Avatar 2 (cheveux rouge)
avatar_3_img_raw = pygame.image.load("image_menu/avatar_3.png")  # Avatar 3 (cheveux brun)
selected_avatar_1_img_raw = pygame.image.load("image_menu/selected_avatar_1.png")  # Avatar 1 selectionné
selected_avatar_2_img_raw = pygame.image.load("image_menu/selected_avatar_2.png")  # Avatar 2 selectionné
selected_avatar_3_img_raw = pygame.image.load("image_menu/selected_avatar_3.png")  # Avatar 3 selectionné

# --- Variables globales pour stocker les images converties ---
menu_bg, guide_bg, game_bg, parameter_on_bg, parameter_off_bg = [None] * 5
violet_ball_img, blue_ball_img, orange_ball_img = [None] * 3
selected_violet_ball_img, selected_blue_ball_img, selected_orange_ball_img = [None] * 3
avatar_1_img, avatar_2_img, avatar_3_img = [None] * 3
selected_avatar_1_img, selected_avatar_2_img, selected_avatar_3_img = [None] * 3


def init_check_events_assets():
    """
    Initialise les assets graphiques gérés par ce module.
    Convertit les images.
    :) help
    """
    global menu_bg, guide_bg, game_bg, parameter_on_bg, parameter_off_bg, violet_ball_img, blue_ball_img, orange_ball_img
    global selected_violet_ball_img, selected_blue_ball_img, selected_orange_ball_img, avatar_1_img, avatar_2_img, avatar_3_img
    global selected_avatar_1_img, selected_avatar_2_img, selected_avatar_3_img

    # Conversion des fonds d'écran
    menu_bg = menu_bg_raw.convert()
    guide_bg = guide_bg_raw.convert()
    game_bg = game_bg_raw.convert()
    parameter_on_bg = parameter_on_bg_raw.convert()
    parameter_off_bg = parameter_off_bg_raw.convert()

    # Conversion des images de ballons et avatars
    violet_ball_img = violet_ball_img_raw.convert_alpha()
    blue_ball_img = blue_ball_img_raw.convert_alpha()
    orange_ball_img = orange_ball_img_raw.convert_alpha()
    selected_violet_ball_img = selected_violet_ball_img_raw.convert_alpha()
    selected_blue_ball_img = selected_blue_ball_img_raw.convert_alpha()
    selected_orange_ball_img = selected_orange_ball_img_raw.convert_alpha()

    avatar_1_img = avatar_1_img_raw.convert_alpha()
    avatar_2_img = avatar_2_img_raw.convert_alpha()
    avatar_3_img = avatar_3_img_raw.convert_alpha()
    selected_avatar_1_img = selected_avatar_1_img_raw.convert_alpha()
    selected_avatar_2_img = selected_avatar_2_img_raw.convert_alpha()
    selected_avatar_3_img = selected_avatar_3_img_raw.convert_alpha()


# --- Définition des rectangles de collision pour les boutons du menu ---
# Ces rectangles sont utilisés pour détecter les clics de souris.
# Coordonnées et dimensions (x, y, largeur, hauteur)
start_button_rect = pygame.Rect(132, 556, 106, 35)  # Bouton "Start"
guide_button_rect = pygame.Rect(382, 556, 119, 35)  # Bouton "Guide"
parameter_button_rect = pygame.Rect(686, 556, 119, 35)  # Bouton "Parameters"
quit_menu_button_rect = pygame.Rect(963, 556, 79, 35)  # Bouton "Quit" sur l'écran de menu

return_menu_button_rect = pygame.Rect(830, 529, 237, 66)  # Bouton "Return to Menu"

# Boutons de contrôle de la musique dans les paramètres
music_on_button_rect = pygame.Rect(829, 189, 76, 41)  # Bouton "Music ON"
music_off_button_rect = pygame.Rect(1002, 189, 76, 41)  # Bouton "Music OFF"

# Boutons de sélection du ballon dans les paramètres
violet_ball_button_rect = pygame.Rect(651, 370, 115, 102)  # Bouton selection balle viollette
blue_ball_button_rect = pygame.Rect(824, 370, 115, 102)  # Bouton selection balle bleu
orange_ball_button_rect = pygame.Rect(996, 370, 115, 102)  # Bouton selection balle orange

# Boutons de sélection de l'avatar dans les paramètres
avatar_1_button_rect = pygame.Rect(89, 243, 115, 178)  # Bouton selection avatar 1
avatar_2_button_rect = pygame.Rect(266, 243, 115, 178)  # Bouton selection avatar 2
avatar_3_button_rect = pygame.Rect(449, 243, 115, 178)  # Bouton selection avatar 3

# Bouton "Quit Game" affiché en jeu
quit_game_button_rect = pygame.Rect(1001, 20, 172, 42)

# --- Variables d'état internes à ce module ---
# Ces variables suivent l'état de l'interface utilisateur gérée par `menu_event`.
_internal_running = True  # Contrôle la boucle principale du jeu
_internal_game_launched = False  # Indique si une partie est considérée comme lancée par le menu
_internal_avatar = 1  # ID de l'avatar sélectionné (par défaut 1)
_internal_ball_path = "image/frames-purple-ball"  # Chemin du ballon sélectionné (par défaut violet)
_music_enabled = True  # État interne de l'activation de la musique
_internal_current_screen = "menu"  # Écran actuellement affiché par le menu ("menu", "guide", "parameter_on/off", "game")
_events_for_game_event = []  # Liste pour stocker les événements Pygame, partagée avec game_event

# Variable pour transmettre l'état de la musique à main.py
music_status_for_main = _music_enabled  # Initialisée avec l'état actuel


def set_game_ended_from_main():
    """
    Fonction Game Over ou Victoire.
    Elle réinitialise l'état interne de `check_events.py` pour le return au menu.
    """
    global _internal_game_launched, _internal_current_screen
    _internal_game_launched = False  # Indiquer que la partie n'est plus lancée
    _internal_current_screen = "menu"  # Revenir à l'écran du menu
    pygame.display.set_caption(f"Dunk & Degree - Menu")  # Met à jour le titre de la fenêtre


def menu_event(SCREEN_WIDTH_UNUSED, SCREEN_HEIGHT_UNUSED, screen_surface_UNUSED):
    """
    Gère tous les événements Pygame pour le menu et les interactions de base.
    Traite les clics de souris pour la navigation dans le menu, la sélection d'options, et le démarrage/arrêt du jeu.

    Args:
        SCREEN_WIDTH_UNUSED, SCREEN_HEIGHT_UNUSED, screen_surface_UNUSED

    Returns:
        tuple: Contient l'état actuel de (_internal_running, _internal_game_launched, _internal_ball_path, _internal_avatar, _internal_current_screen, music_status_for_main).
    """
    global _internal_running, _internal_current_screen, _internal_game_launched, _internal_avatar
    global _internal_ball_path, _music_enabled, _events_for_game_event, music_status_for_main

    pos = None  # Variable pour stocker la position du clic de souris
    _events_for_game_event = pygame.event.get()  # Récupérer tous les événements de la file d'attente

    for event in _events_for_game_event:
        if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
            _internal_running = False  # Signaler l'arrêt du jeu

        if event.type == pygame.MOUSEBUTTONDOWN:  # Si un bouton de la souris est cliqué
            # Enregistrer la position du clic si:
            # 1. Le jeu n'est pas lancé (on est dans le menu/guide/paramètres).
            # OU 2. Le jeu est lancé ET le clic est sur le bouton "Quit Game" en jeu.
            if not _internal_game_launched or (_internal_game_launched and quit_game_button_rect.collidepoint(event.pos)):
                pos = event.pos

        if pos is not None:  # Si un clic pertinent a été détecté
            prev_screen = _internal_current_screen  # Sauvegarder l'écran précédent pour comparaison

            # --- Logique de navigation basée sur l'écran actuel ---
            if _internal_current_screen == "menu":
                if start_button_rect.collidepoint(pos):
                    _internal_current_screen = "game"
                    _internal_game_launched = True  # Lancer le jeu
                elif guide_button_rect.collidepoint(pos):
                    _internal_current_screen = "guide"  # Aller à l'écran du guide
                elif parameter_button_rect.collidepoint(pos):
                    # Aller à l'écran des paramètres, en choisissant le fond basé sur l'état actuel de la musique
                    _internal_current_screen = "parameter_on" if _music_enabled else "parameter_off"
                elif quit_menu_button_rect.collidepoint(pos):
                    _internal_running = False  # Quitter le jeu

            elif _internal_current_screen == "guide":
                if return_menu_button_rect.collidepoint(pos):  # Bouton "Return to Menu"
                    _internal_current_screen = "menu"

            elif _internal_current_screen in ["parameter_on", "parameter_off"]:  # Écran des paramètres
                if return_menu_button_rect.collidepoint(pos):  # Bouton "Return to Menu"
                    _internal_current_screen = "menu"

                # --- Gestion des boutons de contrôle de la musique ---
                if _music_enabled and music_off_button_rect.collidepoint(pos):  # Si musique ON et clic sur OFF
                    _music_enabled = False  # Désactiver la musique
                    sound_manager.stop_music()  # Arrêter la musique immédiatement
                    _internal_current_screen = "parameter_off"  # Changer le fond d'écran des paramètres
                elif not _music_enabled and music_on_button_rect.collidepoint(pos):  # Si musique OFF et clic sur ON
                    _music_enabled = True  # Activer la musique
                    # La musique sera relancée par main.py via play_appropriate_music()
                    # pour correspondre à l'état actuel (menu ou jeu).
                    _internal_current_screen = "parameter_on"  # Changer le fond d'écran des paramètres

                # --- Gestion de la sélection de l'avatar ---
                if avatar_1_button_rect.collidepoint(pos):
                    _internal_avatar = 1
                elif avatar_2_button_rect.collidepoint(pos):
                    _internal_avatar = 2
                elif avatar_3_button_rect.collidepoint(pos):
                    _internal_avatar = 3

                # --- Gestion de la sélection du ballon ---
                if violet_ball_button_rect.collidepoint(pos):
                    _internal_ball_path = "image/frames-purple-ball"
                elif blue_ball_button_rect.collidepoint(pos):
                    _internal_ball_path = "image/frames-blue-ball"
                elif orange_ball_button_rect.collidepoint(pos):
                    _internal_ball_path = "image/frames-orange-ball"

            # Ce cas gère le clic sur le bouton "Quit Game" depuis l'overlay du jeu
            elif _internal_current_screen == "game" and _internal_game_launched:
                if quit_game_button_rect.collidepoint(pos):
                    _internal_current_screen = "menu"  # Revenir au menu
                    _internal_game_launched = False  # Signaler que le jeu n'est plus lancé

            # Mettre à jour le titre de la fenêtre si l'écran a changé
            if prev_screen != _internal_current_screen and _internal_current_screen != "game":
                new_caption = f"Dunk & Degree - {_internal_current_screen.replace('_', ' ').title()}"
                pygame.display.set_caption(new_caption)
            elif _internal_current_screen == "game" and _internal_game_launched:  # Titre spécifique pour le jeu
                pygame.display.set_caption("Dunk & Degree - Playing")

            pos = None  # Réinitialiser la position du clic après traitement

    music_status_for_main = _music_enabled  # Mettre à jour le statut de la musique pour main.py

    return _internal_running, _internal_game_launched, _internal_ball_path, _internal_avatar, _internal_current_screen, music_status_for_main


def show_img(s, ui_state_for_background):
    """
    Affiche le fond d'écran approprié sur la surface donnée.
    Le fond des paramètres dépend de l'état `_music_enabled`.

    Args:
        s : La surface sur laquelle dessiner (généralement l'écran principal).
        ui_state_for_background (str): L'état de l'interface utilisateur qui détermine quel fond afficher.
    """
    # Affichage du fond des paramètres
    # pour s'assurer qu'on est bien sur l'écran des paramètres.
    if ui_state_for_background == "parameter_on":  # Si l'intention est d'afficher "parameter_on"
        s.blit(parameter_on_bg if _music_enabled else parameter_off_bg, (0, 0))
    elif ui_state_for_background == "parameter_off":  # Si l'intention est d'afficher "parameter_off"
        s.blit(parameter_off_bg if not _music_enabled else parameter_on_bg, (0, 0))
    # Autres fonds d'écran
    elif ui_state_for_background == "menu" and menu_bg:
        s.blit(menu_bg, (0, 0))
    elif ui_state_for_background == "guide" and guide_bg:
        s.blit(guide_bg, (0, 0))
    elif ui_state_for_background == "game" and game_bg:
        s.blit(game_bg, (0, 0))


def show_overlay(s, ui_state_from_menu_event, avatar_id, ball_path):
    """
    Affiche les éléments d'overlay, spécifiquement les sélections d'avatar et de ballon
    sur l'écran des paramètres.

    Args:
        s : La surface sur laquelle dessiner.
        ui_state_from_menu_event (str): L'état actuel de l'interface du menu.
        avatar_id (int): L'ID de l'avatar actuellement sélectionné.
        ball_path (str): Le chemin du ballon actuellement sélectionné.
    """
    # L'overlay des sélections n'est pertinent que sur l'écran des paramètres
    if ui_state_from_menu_event in ["parameter_on", "parameter_off"]:
        if not avatar_1_img:
            return  # S'assurer que les images sont chargées pour éviter une erreur

        # Déterminer quelles images d'avatar afficher (sélectionnée ou non sélectionnée)
        current_avatar_display_tuple = (selected_avatar_1_img, avatar_2_img, avatar_3_img)  # Par défaut, avatar 1 est sélectionné
        if avatar_id == 2:
            current_avatar_display_tuple = (avatar_1_img, selected_avatar_2_img, avatar_3_img)
        elif avatar_id == 3:
            current_avatar_display_tuple = (avatar_1_img, avatar_2_img, selected_avatar_3_img)

        # Afficher les images des avatars aux positions prédéfinies
        s.blit(current_avatar_display_tuple[0], (66, 238))
        s.blit(current_avatar_display_tuple[1], (239, 238))
        s.blit(current_avatar_display_tuple[2], (411, 238))

        # Déterminer quelles images de ballon afficher
        current_ball_display_tuple = (
        selected_violet_ball_img, blue_ball_img, orange_ball_img)  # Par défaut, ballon violet
        if ball_path == "image/frames-blue-ball":
            current_ball_display_tuple = (violet_ball_img, selected_blue_ball_img, orange_ball_img)
        elif ball_path == "image/frames-orange-ball":
            current_ball_display_tuple = (violet_ball_img, blue_ball_img, selected_orange_ball_img)

        # Afficher les images des ballons aux positions prédéfinies
        s.blit(current_ball_display_tuple[0], (636, 354))
        s.blit(current_ball_display_tuple[1], (810, 354))
        s.blit(current_ball_display_tuple[2], (985, 354))


def game_event(ball_state, current_game_play_state_from_main):
    """
    Gère les événements spécifiques au gameplay (entrées clavier pour le ballon).

    Args:
        ball_state (dict): L'état actuel du ballon (pour ajuster angle, vitesse, lancer).
        current_game_play_state_from_main (str): L'état de jeu actuel transmis par `main.py`. Les actions ne sont traitées que si "playing".

    Returns:
        bool: True si le jeu doit continuer, False s'il doit s'arrêter.
    """
    global _events_for_game_event  # Utilise la liste d'événements capturée par menu_event

    # Ne traiter les entrées de jeu que si l'état est "playing"
    if current_game_play_state_from_main != "playing":
        _events_for_game_event = []  # Vider les événements pour éviter des entrées périmées plus tard
        return True  # Continuer le jeu

    running_status = True  # Par défaut, le jeu continue
    for e in _events_for_game_event:  # Parcourir les événements récupérés
        if e.type == pygame.QUIT:
            running_status = False

        if e.type == pygame.KEYDOWN:  # Si une touche est pressée
            if e.key == pygame.K_SPACE:  # Espace pour lancer le ballon
                launch_ball(ball_state)
            elif e.key == pygame.K_UP:  # Flèche haut pour augmenter l'angle
                adjust_ball_angle(ball_state, "up")
            elif e.key == pygame.K_DOWN:  # Flèche bas pour diminuer l'angle
                adjust_ball_angle(ball_state, "down")
            elif e.key == pygame.K_LEFT:  # Flèche gauche pour diminuer la vélocité
                adjust_ball_velocity(ball_state, "left")
            elif e.key == pygame.K_RIGHT:  # Flèche droite pour augmenter la vélocité
                adjust_ball_velocity(ball_state, "right")

    _events_for_game_event = []  # Vider la liste d'événements
    return running_status