# main.py
# Fichier principal du jeu "Dunk & Degree"
# Gère la boucle de jeu principale, les états du jeu, le score, les niveaux, l'orchestration des différents modules

import pygame
import time

# Initialisation de Pygame et de ses modules
pygame.init()

# Importation des modules personnalisés du jeu
from check_events import *
from level import *
from trajectory import *
import sound_manager

# Constantes pour la taille de l'écran
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675
# Création de la surface principale de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Définition du titre de la fenêtre
pygame.display.set_caption("Dunk & Degree")

# Initialisation des assets
init_check_events_assets()
init_level_assets(SCREEN_WIDTH, SCREEN_HEIGHT)
# Initialisation du mixer Pygame pour le son
sound_manager.init_mixer()

# Variables pour les écrans de fin de jeu (victoire et défaite)
winner_screen_image = pygame.image.load("image/winner_screen.jpg").convert()
game_over_lose_screen_image = pygame.image.load("image/game_over_screen.jpg").convert()

# Initialisation de l'état du ballon (position, vitesse, etc.)
ball_state = reset_ball_state(SCREEN_WIDTH, SCREEN_HEIGHT)

# Variables de contrôle du jeu
running = True  # Booléen pour contrôler la boucle principale du jeu
game_launched = False  # Booléen pour indiquer si une partie est en cours
game_assets_loaded = False  # Booléen pour indiquer si les assets spécifiques à la partie (ballon, avatar) sont chargés

# Constantes pour les états de jeu
GAME_STATE_MENU = "menu_ui"  # Le jeu est dans le menu
GAME_STATE_PLAYING = "playing"  # Le jeu est en cours (phase de jeu active)
GAME_STATE_LEVEL_TRANSITION = "level_transition"  # Phase de transition entre les niveaux
GAME_STATE_GAME_OVER_TIME = "game_over_time"  # Fin de partie car temps écoulé
GAME_STATE_GAME_OVER_WIN = "game_over_win"  # Fin de partie car tous les niveaux sont terminés
current_game_play_state = GAME_STATE_MENU  # État de jeu actuel, commence par le menu

# Variables de jeu
difficulty_selector = 0  # Index du sélecteur de difficulté (0: Facile, 1: Normal, etc.)
level_value = 0  # Index du niveau actuel au sein de la difficulté sélectionnée
score = 0  # Score du joueur
current_ball_path = "image/frames-purple-ball"  # Chemin vers les frames du ballon actuellement sélectionné automatiquement
current_avatar_id = 1  # ID de l'avatar actuellement sélectionné automatiquement
selected_avatar_imgs = None  # Surface des images de l'avatar sélectionné (chargées au lancement du jeu)

# Horloge Pygame pour contrôler la vitesse du jeu (FPS)
clock = pygame.time.Clock()

# Constantes et variables de temps pour les niveaux
LEVEL_DURATION = 30  # Durée d'un niveau en secondes
level_start_time = 0  # Timestamp du début du niveau actuel
time_remaining = LEVEL_DURATION  # Temps restant pour le niveau actuel
basket_scored_this_level = False  # Booléen pour savoir si un panier a été marqué dans le niveau actuel

# Constantes et variables pour la transition entre les niveaux
LEVEL_TRANSITION_DURATION = 3000  # Durée de l'écran de transition en millisecondes
level_transition_start_time = 0  # Timestamp du début de la transition

# Constantes et variables pour l'affichage du message de Game Over
GAME_OVER_MESSAGE_DURATION = 3000  # Durée d'affichage de l'écran Game Over avant retour au menu
game_over_time_display_start = 0  # Timestamp du début de l'affichage du Game Over

# Activation de la musique
music_is_globally_enabled = True

# La zone de collision du panier pour marquer
HOOP_OFFSET_X = 55  # Décalage en X par rapport à la position du panier (basket_current_x)
HOOP_OFFSET_Y = 45  # Décalage en Y
HOOP_WIDTH = 90  # Largeur du panier
HOOP_HEIGHT = 30  # Hauteur du panier

# Polices de caractères pour l'affichage du texte
score_font = pygame.font.Font(None, 60)  # Pour le score
timer_font = pygame.font.Font(None, 60)  # Pour le chronomètre
message_font = pygame.font.Font(None, 80)  # Pour les messages importants
small_message_font = pygame.font.Font(None, 40)  # Pour les messages plus petits
final_score_font = pygame.font.Font(None, 70)  # Pour le score final sur l'écran de Game Over

# Variables pour stocker la position actuelle du panier
basket_current_x = 0
basket_current_y = 0

# Variable pour suivre l'état de l'interface utilisateur du menu
current_ui_state_from_menu = "menu"  # Commence par l'écran principal du menu

# Gestion des images de transition de niveau
LEVEL_TRANSITION_IMAGE_PATH = "image/level_screens/"  # Chemin vers le dossier des images de transition
level_transition_images = {}  # Dictionnaire pour stocker les images de transition
current_level_transition_image = None  # Image de transition actuellement affichée


def get_global_level_number(cur_diff_sel, cur_lvl_val):
    """
    Calcule le numéro de niveau global basé sur la difficulté et le niveau actuel dans cette difficulté.
    Permet d'avoir un affichage "Niveau X" continu à travers les difficultés.
    Args:
        cur_diff_sel (int): Index de la difficulté actuelle.
        cur_lvl_val (int): Index du niveau actuel dans cette difficulté.
    Returns:
        int: Le numéro de niveau global.
    """
    gl = 0
    # Nombre de niveaux par difficulté précédente: Easy(3), Normal(3), Intermediate(3), Difficult(5)
    if cur_diff_sel == 0:  # Easy
        gl = cur_lvl_val + 1
    elif cur_diff_sel == 1:  # Normal (après 3 niveaux Easy)
        gl = 3 + cur_lvl_val + 1
    elif cur_diff_sel == 2:  # Intermediate (après 3 Easy + 3 Normal)
        gl = 3 + 3 + cur_lvl_val + 1
    elif cur_diff_sel == 3:  # Difficult (après 3 Easy + 3 Normal + 3 Intermediate)
        gl = 3 + 3 + 3 + cur_lvl_val + 1
    return gl


def load_level_transition_image(gl_lvl_num):
    """
    Charge (ou récupère depuis le cache) l'image de transition pour un numéro de niveau global donné.
    Args:
        gl_lvl_num (int): Le numéro de niveau global.
    Returns:
        pygame.Surface: L'image de transition chargée ou une image de remplacement.
    """
    global level_transition_images  # Accès au cache d'images
    # Si l'image est déjà en cache, la retourner
    if gl_lvl_num in level_transition_images :
        return level_transition_images[gl_lvl_num]

    # Construire le nom de fichier de l'image
    img_fname = f"level_{gl_lvl_num}.jpg"
    fp = os.path.join(LEVEL_TRANSITION_IMAGE_PATH, img_fname)
    # Charger l'image, la convertir et la redimensionner
    img = pygame.image.load(fp).convert()
    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    level_transition_images[gl_lvl_num] = img  # Mettre en cache
    return img

def play_appropriate_music():
    """
    Joue la musique appropriée en fonction de l'état actuel du jeu et de la difficulté.
    Gère également l'activation/désactivation globale de la musique.
    """
    global difficulty_selector, current_game_play_state, music_is_globally_enabled

    # Si la musique est globalement désactivée
    if not music_is_globally_enabled:
        if sound_manager.is_playing():  # Si une musique est en cours
            sound_manager.stop_music()  # L'arrêter
        return  # Ne rien jouer

    # Déterminer la clé de la musique à jouer
    target_music_key = None
    loops = -1  # Nombre de répétitions (-1 pour infini)
    volume = 0.5  # Volume par défaut
    if current_game_play_state == GAME_STATE_MENU:
        target_music_key = "menu"
    elif current_game_play_state == GAME_STATE_PLAYING or current_game_play_state == GAME_STATE_LEVEL_TRANSITION:
        # Musique basée sur le palier de difficulté
        if difficulty_selector == 0:
            target_music_key = "palier1_easy"
        elif difficulty_selector == 1:
            target_music_key = "palier2_normal"
        elif difficulty_selector == 2:
            target_music_key = "palier3_intermediate"
        elif difficulty_selector == 3:
            target_music_key = "palier4_difficult"
    elif current_game_play_state == GAME_STATE_GAME_OVER_WIN:
        target_music_key = "score_fin_win"
        loops = 0  # Jouer une seule fois
    elif current_game_play_state == GAME_STATE_GAME_OVER_TIME:
        target_music_key = "game_over_lose"
        loops = 0  # Jouer une seule fois

    # Jouer la musique si une clé a été déterminée et qu'elle n'est pas déjà en cours
    if target_music_key and not sound_manager.is_playing(target_music_key):
        sound_manager.play_music(target_music_key, loops=loops, volume=volume)
    # Si aucune musique cible n'est définie (ex: état non géré) et qu'on n'est pas en transition de niveau
    elif not target_music_key and current_game_play_state != GAME_STATE_LEVEL_TRANSITION:
        if sound_manager.is_playing(): sound_manager.stop_music()  # Arrêter la musique en cours


def start_new_level_setup():
    """
    initialise les paramètres pour un nouveau niveau.
    Passe à l'état de transition de niveau.
    """
    global basket_scored_this_level, ball_state, current_game_play_state, game_assets_loaded
    global current_ball_path, difficulty_selector, level_value, current_level_transition_image
    global level_transition_start_time, level_start_time, time_remaining

    basket_scored_this_level = False  # Réinitialiser le flag de panier marqué pour le niveau
    ball_state = reset_ball_state(SCREEN_WIDTH, SCREEN_HEIGHT)  # Réinitialiser l'état du ballon
    # Positionner le panier selon la difficulté et le niveau
    reset_basket_position_for_level(difficulty_selector, level_value, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Recharger les frames du ballon si les assets de jeu étaient déjà chargés et que les frames sont manquantes/vides
    if game_assets_loaded and (not ball_state["frames"] or ball_state["frames"] == []):
        ball_state["frames"] = load_ball_frames(current_ball_path)
    if not ball_state["frames"]:
        print("ERROR FATAL: Rechargement frames balle.")  # Erreur critique si échec

    # Charger l'image de transition pour le niveau global actuel
    gl_lvl = get_global_level_number(difficulty_selector, level_value)
    current_level_transition_image = load_level_transition_image(gl_lvl)

    # Passer à l'état de transition de niveau et enregistrer le temps de début
    current_game_play_state = GAME_STATE_LEVEL_TRANSITION
    level_transition_start_time = pygame.time.get_ticks()

    # Réinitialiser les variables du minuteur de niveau (elles seront effectivement utilisées après la transition)
    level_start_time = 0
    time_remaining = LEVEL_DURATION

    play_appropriate_music()  # Jouer la musique appropriée (celle du palier ou de transition)


def advance_to_next_challenge():
    """
    Passe au niveau suivant ou à la difficulté suivante si le niveau actuel est terminé.
    Si tous les niveaux de toutes les difficultés sont terminés, passe à l'écran de victoire.
    """
    global level_value, difficulty_selector, current_game_play_state

    # Définition du nombre maximum de niveaux pour chaque difficulté (0-indexé pour la valeur max)
    # Easy (3 niveaux: 0, 1, 2), Normal (3), Intermediate (3), Difficult (5)
    max_levels_map = {"Easy": 3, "Normal": 3, "Intermediate": 3, "Difficult": 5}
    current_difficulty_name = difficulty[difficulty_selector]  # Nom de la difficulté actuelle
    max_lvl_for_current_difficulty = max_levels_map.get(current_difficulty_name, 3)  # Nombre de niveaux

    # Si ce n'est pas le dernier niveau de la difficulté actuelle
    if level_value < max_lvl_for_current_difficulty - 1:
        level_value += 1  # Passer au niveau suivant
        start_new_level_setup()  # Configurer le nouveau niveau
    else:  # C'est le dernier niveau de la difficulté actuelle
        # Si ce n'est pas la dernière difficulté
        if difficulty_selector < len(difficulty) - 1:
            difficulty_selector += 1  # Passer à la difficulté suivante
            level_value = 0  # Recommencer au premier niveau de cette nouvelle difficulté
            start_new_level_setup()  # Configurer le nouveau niveau
        else:  # Toutes les difficultés sont terminées
            print("GAME COMPLETED!")
            current_game_play_state = GAME_STATE_GAME_OVER_WIN  # Passer à l'écran de victoire
            play_appropriate_music()  # Jouer la musique de victoire


def display_centered_message(txt, fnt, col=(255, 255, 255), y_off=0, aa=True):
    """
    Affiche un message textuel centré sur l'écran.
    Args:
        txt (str): Le texte à afficher.
        fnt (pygame.font.Font): La police à utiliser.
        col (tuple, optional): La couleur du texte. Par défaut (255, 255, 255) (blanc).
        y_off (int, optional): Décalage vertical par rapport au centre. Par défaut 0.
        aa (bool, optional): Anti-aliasing pour le texte. Par défaut True.
    """
    s = fnt.render(txt, aa, col)  # Rendu du texte en surface
    r = s.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_off))  # Obtenir le rectangle et le centrer
    screen.blit(s, r)  # Afficher la surface sur l'écran principal


# Lancer la musique du menu au démarrage du jeu
play_appropriate_music()

# ----- BOUCLE DE JEU PRINCIPALE -----
while running:
    # --- Gestion des événements du menu/jeu via check_events.py ---
    # menu_event gère les clics, les changements d'écran du menu, et retourne l'état actuel.
    # Il récupère aussi tous les événements Pygame pour que game_event puisse les utiliser.
    new_running, should_game_be_launched, new_bpath, new_aid, current_ui_state_from_menu, music_enabled_from_menu = menu_event(
        SCREEN_WIDTH, SCREEN_HEIGHT, screen)

    running = new_running  # Mettre à jour l'état de la boucle principale (si l'utilisateur quitte)
    current_ball_path = new_bpath  # Mettre à jour le ballon sélectionné
    current_avatar_id = new_aid  # Mettre à jour l'ID de l'avatar sélectionné

    # --- Gestion de l'état global de la musique ---
    # Si l'état de la musique a changé via le menu (boutons ON/OFF)
    if music_is_globally_enabled != music_enabled_from_menu:
        music_is_globally_enabled = music_enabled_from_menu  # Mettre à jour le flag global
        play_appropriate_music()  # Mettre à jour la lecture de la musique en conséquence

    # --- Gestion du lancement/arrêt de la partie ---
    # Si l'état de `game_launched` (partie en cours) a changé
    if game_launched != should_game_be_launched:
        game_launched = should_game_be_launched  # Mettre à jour l'état
        if game_launched:  # Si une partie est lancée/recommencée
            game_assets_loaded = False  #Réinitialisation des assets de jeu
            score = 0  # Réinitialiser le score
            level_value = 0  # Réinitialiser le niveau
            difficulty_selector = 0  # Réinitialiser la difficulté au premier palier
            start_new_level_setup()  # Commencer la configuration du premier niveau
        else:  # Si une partie est arrêtée (retour au menu depuis le jeu ou Game Over)
            game_assets_loaded = False  # Marquer les assets de jeu comme non chargés
            selected_avatar_imgs = None  # Libérer les images de l'avatar
            current_game_play_state = GAME_STATE_MENU  # Revenir à l'état du menu
            play_appropriate_music()  # Jouer la musique du menu
            if "frames" in ball_state:
                ball_state["frames"] = []  # Vider les frames du ballon

    # --- Détermination du fond d'écran à afficher ---
    background_to_show = "menu"  # Par défaut, fond du menu
    if game_launched:
        background_to_show = "game"  # Si une partie est lancée, fond du jeu
    else:  # Si pas de partie lancée (dans le menu, ou transition vers le menu)
        background_to_show = current_ui_state_from_menu  # Fond basé sur l'écran actuel du menu (menu, guide, paramètres)
        if current_game_play_state != GAME_STATE_MENU:
            # Ce cas gère la situation où l'on quitte une partie
            # La logique de Game Over définit maintenant explicitement l'état à MENU.
            current_game_play_state = GAME_STATE_MENU
            play_appropriate_music()  # Assurer la musique du menu
        # Si déjà dans l'état menu et que la musique du menu ne joue pas (ex: après un changement dans les paramètres)
        elif sound_manager.current_music_key != "menu" and current_ui_state_from_menu == "menu" and music_is_globally_enabled:
            play_appropriate_music()

    # --- Affichage du fond d'écran et des overlays (si applicable) ---
    if current_game_play_state not in [GAME_STATE_GAME_OVER_WIN, GAME_STATE_GAME_OVER_TIME, GAME_STATE_LEVEL_TRANSITION]:
        show_img(screen, background_to_show)  # Affiche le fond d'écran déterminé

    # Affiche les overlays (comme les sélections d'avatar/ballon dans les paramètres)
    # uniquement si on est dans le menu ou les écrans de paramètres.
    if current_game_play_state == GAME_STATE_MENU or current_ui_state_from_menu in ["parameter_on", "parameter_off"]:
        show_overlay(screen, current_ui_state_from_menu, current_avatar_id, current_ball_path)

    # --- LOGIQUE DE JEU SI UNE PARTIE EST LANCÉE ---
    if game_launched:
        # Chargement des assets spécifiques à la partie (ballon, avatar) si pas encore fait
        # et si on est sur le point d'entrer en phase de jeu active.
        if not game_assets_loaded and current_game_play_state == GAME_STATE_PLAYING:
            ball_state["frames"] = load_ball_frames(current_ball_path)  # Charger les frames du ballon
            selected_avatar_imgs = load_avatar(current_avatar_id)  # Charger les images de l'avatar
            if not selected_avatar_imgs or not ball_state["frames"]:  # Erreur critique si échec
                print("ERR FATAL: Assets jeu NI.")
                running = False
            else:
                game_assets_loaded = True  # Marquer les assets comme chargés

        # Exécuter la logique de jeu si les assets sont chargés OU si l'état de jeu ne les requiert pas immédiatement (transition, game over).
        if game_assets_loaded or current_game_play_state in [GAME_STATE_LEVEL_TRANSITION, GAME_STATE_GAME_OVER_TIME, GAME_STATE_GAME_OVER_WIN]:
            # === ÉTAT: EN JEU ===
            if current_game_play_state == GAME_STATE_PLAYING:
                # Vérification de sécurité pour s'assurer que les assets sont chargés
                if not game_assets_loaded:
                    ball_state["frames"] = load_ball_frames(current_ball_path)
                    selected_avatar_imgs = load_avatar(current_avatar_id)
                    if not selected_avatar_imgs or not ball_state["frames"]:
                        print("ERR FATAL: Assets jeu NI during play.")
                        running = False
                        continue  # Arrêter si erreur
                    game_assets_loaded = True

                # S'assurer que la musique du palier actuel est jouée si la musique est activée
                if music_is_globally_enabled:
                    palier_music_key = None  # Déterminer la clé de musique du palier
                    if difficulty_selector == 0:
                        palier_music_key = "palier1_easy"
                    elif difficulty_selector == 1:
                        palier_music_key = "palier2_normal"
                    elif difficulty_selector == 2:
                        palier_music_key = "palier3_intermediate"
                    elif difficulty_selector == 3:
                        palier_music_key = "palier4_difficult"
                    if palier_music_key and not sound_manager.is_playing(palier_music_key):
                        play_appropriate_music()  # Jouer la musique si ce n'est pas déjà fait

                # Calcul du temps écoulé et du temps restant pour le niveau
                el_time = time.time() - level_start_time
                time_remaining = max(0, LEVEL_DURATION - int(el_time))

                # Afficher le fond d'écran du jeu si show_img ne l'a pas fait plus haut
                # (ceci assure que le fond est dessiné avant les éléments de jeu)
                if background_to_show == "game":
                    show_img(screen, "game")

                # Mettre à jour et afficher le panier
                basket_current_x, basket_current_y = basket_hoop(screen, difficulty_selector, level_value, SCREEN_WIDTH,
                                                                 SCREEN_HEIGHT)
                # Mettre à jour la physique et l'animation du ballon
                update_ball(ball_state, SCREEN_WIDTH, SCREEN_HEIGHT, current_ball_path)
                # Dessiner l'avatar et le ballon
                if selected_avatar_imgs: draw_ball(screen, ball_state, selected_avatar_imgs)

                # Informations sur la zone de collision du panier (hoop)
                hoop_info = {"x": basket_current_x + HOOP_OFFSET_X, "y": basket_current_y + HOOP_OFFSET_Y,"width": HOOP_WIDTH, "height": HOOP_HEIGHT}
                # Dessiner la trajectoire prédictive du ballon
                draw_trajectory_dots(screen, ball_state, SCREEN_WIDTH, SCREEN_HEIGHT, hoop_info)

                # Détection de panier marqué
                if ball_state["shooting"] and not ball_state["scored_this_throw"]:  # Si le ballon est en l'air et n'a pas encore marqué ce tir
                    if ball_state["frames"] and len(ball_state["frames"]) > 0:
                        # S'assurer que les coordonnées du ballon sont valides
                        current_ball_x = ball_state.get("x", 0)
                        current_ball_y = ball_state.get("y", 0)
                        if isinstance(current_ball_x, (int, float)) and isinstance(current_ball_y, (int, float)):
                            b_rect = ball_state["frames"][0].get_rect(
                                topleft=(current_ball_x, current_ball_y))  # Rectangle du ballon
                            h_rect = pygame.Rect(hoop_info["x"], hoop_info["y"], hoop_info["width"],hoop_info["height"])  # Rectangle du hoop
                            # Si le centre du ballon entre en collision avec le panier ET que le ballon descend (vy_physics < ~0)
                            if h_rect.collidepoint(b_rect.centerx, b_rect.centery) and ball_state.get("vy_physics",1) < -0.01:
                                score += 1  # Augmenter le score
                                ball_state["scored_this_throw"] = True  # Marquer ce tir comme réussi
                                basket_scored_this_level = True  # Indiquer qu'un panier a été marqué dans ce niveau

                # Gestion de la fin du temps pour le niveau
                if time_remaining <= 0:
                    if basket_scored_this_level:  # Si un panier a été marqué
                        advance_to_next_challenge()  # Passer au niveau/difficulté suivant(e)
                    else:  # Si aucun panier n'a été marqué
                        current_game_play_state = GAME_STATE_GAME_OVER_TIME  # Game Over
                        game_over_time_display_start = pygame.time.get_ticks()  # Démarrer le minuteur d'affichage du Game Over
                        play_appropriate_music()  # Jouer la musique de Game Over

                # Gestion des événements spécifiques au jeu (lancer, ajuster angle/vitesse)
                current_running_status = game_event(ball_state, current_game_play_state)
                if not current_running_status: running = False  # Si game_event signale l'arrêt du jeu

                # Affichage des informations de jeu (score, niveau, temps)
                s_surf = score_font.render(f"Score: {score}", True, (255, 255, 255))
                screen.blit(s_surf, (10, 10))  # Score en haut à gauche
                gl_lvl = get_global_level_number(difficulty_selector, level_value)
                lvl_txt = f"Level {gl_lvl}"
                lvl_s = score_font.render(lvl_txt, True, (255, 255, 255))
                lvl_r = lvl_s.get_rect(midtop=(SCREEN_WIDTH // 2, 10))
                screen.blit(lvl_s, lvl_r)  # Numéro de niveau en haut au centre
                t_surf = timer_font.render(f"Time: {time_remaining}", True, (255, 255, 0))
                t_r = t_surf.get_rect(topright=(SCREEN_WIDTH - 30,  70))
                screen.blit(t_surf, t_r)  # Temps restant en haut à droite en dessous du bouton quit

            # === ÉTAT: TRANSITION DE NIVEAU ===
            elif current_game_play_state == GAME_STATE_LEVEL_TRANSITION:
                screen.blit(current_level_transition_image, (0, 0))  # L'afficher

                # Vérifier si la durée de la transition est écoulée
                cur_ticks = pygame.time.get_ticks()
                if cur_ticks - level_transition_start_time >= LEVEL_TRANSITION_DURATION:
                    level_start_time = time.time()  # Démarrer le chronomètre pour le niveau qui commence
                    # time_remaining est déjà initialisé dans start_new_level_setup
                    basket_scored_this_level = False  # Réinitialiser pour le nouveau niveau
                    current_game_play_state = GAME_STATE_PLAYING  # Passer à l'état de jeu actif
                    game_assets_loaded = False  # S'assurer que les assets sont (re)chargés si nécessaire pour le niveau
                    play_appropriate_music()  # Jouer la musique du palier qui commence

                # Gestion minimale des événements pendant la transition (juste pour quitter)
                for ev_t in pygame.event.get():
                    if ev_t.type == pygame.QUIT: running = False

            # === ÉTAT: GAME OVER (TEMPS ÉCOULÉ) ===
            elif current_game_play_state == GAME_STATE_GAME_OVER_TIME:
                if game_over_lose_screen_image:  # Si l'image de Game Over est chargée
                    screen.blit(game_over_lose_screen_image, (0, 0))  # L'afficher
                # Le texte de remplacement est déjà inclus dans game_over_lose_screen_image si le chargement a échoué

                # Afficher le score final
                final_score_text = f"Final score: {score}"
                display_centered_message(final_score_text, final_score_font, (230, 230, 230), SCREEN_HEIGHT * 0.25)

                # Vérifier si la durée d'affichage du message de Game Over est écoulée
                current_ticks_for_game_over_display = pygame.time.get_ticks()
                if current_ticks_for_game_over_display - game_over_time_display_start >= GAME_OVER_MESSAGE_DURATION:
                    game_launched = False  # Signaler que la session de jeu est terminée
                    current_game_play_state = GAME_STATE_MENU  # Revenir à l'état du menu
                    set_game_ended_from_main()  # Synchroniser l'état avec check_events.py
                    play_appropriate_music()  # Jouer la musique du menu

                # Gestion minimale des événements (juste pour quitter)
                for ev_go in pygame.event.get():
                    if ev_go.type == pygame.QUIT: running = False

            # === ÉTAT: GAME OVER (VICTOIRE) ===
            elif current_game_play_state == GAME_STATE_GAME_OVER_WIN:
                if winner_screen_image:
                    screen.blit(winner_screen_image, (0, 0))  # Afficher l'écran de victoire
                # Gestion des événements pour quitter l'écran de victoire (ESC ou Entrée)
                for ev_win in pygame.event.get():
                    if ev_win.type == pygame.QUIT:
                        running = False
                    if ev_win.type == pygame.KEYDOWN:
                        if ev_win.key == pygame.K_ESCAPE or ev_win.key == pygame.K_RETURN:
                            game_launched = False  # Signaler la fin de la session de jeu
                            current_game_play_state = GAME_STATE_MENU  # Revenir à l'état du menu
                            set_game_ended_from_main()  # Synchroniser avec check_events.py
                            play_appropriate_music()  # Jouer la musique du menu
                            break  # Sortir de la boucle d'événements pour cet état

    # Si la partie n'est plus lancée mais que les assets de jeu étaient chargés
    elif not game_launched and game_assets_loaded:
        game_assets_loaded = False  # Marquer comme non chargés
        selected_avatar_imgs = None  # Libérer les images de l'avatar
        if "frames" in ball_state:
            ball_state["frames"] = []  # Vider les frames du ballon

    # Mettre à jour l'affichage complet de l'écran
    pygame.display.flip()
    # Contrôler la vitesse du jeu à 60 images par seconde
    clock.tick(60)

# Quitter Pygame proprement lorsque la boucle principale se termine
pygame.quit()