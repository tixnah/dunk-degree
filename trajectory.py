# trajectory.py
# Gère la logique du ballon de basket et de l'avatar qui le lance.
# Inclut le chargement des images (avatar, frames du ballon), la physique du lancer (trajectoire), l'animation du ballon, le dessin du ballon et de l'avatar, et la prévisualisation de la trajectoire.

import pygame
import os
import math


def load_avatar(avatar_id):
    """
    Charge les images d'un avatar spécifique.

    Args:
        avatar_id (int): L'identifiant de l'avatar à charger (1, 2, ou 3).

    Returns:
        dict: Un dictionnaire contenant les surfaces Pygame pour "side" (côté) et "lance" (lancer), ou None si l'ID est inconnu ou si une erreur de chargement survient.
    """
    imgs = {}  # Dictionnaire pour stocker les images chargées
    base = "image/"  # Dossier de base pour les images d'avatar
    try:
        # Déterminer le préfixe du nom de fichier de l'avatar en fonction de l'ID
        p = "perso1" if avatar_id == 2 else "pers2" if avatar_id == 1 else "pers3" if avatar_id == 3 else None
        if not p:
            print(f"Avatar ID {avatar_id} inconnu.")
            return None

        # Charger, convertir avec alpha et redimensionner les images
        # Image de l'avatar de côté (posture par défaut)
        imgs["side"] = pygame.transform.scale(pygame.image.load(os.path.join(base, f"{p}side.png")).convert_alpha(),(200, 200))
        # Image de l'avatar en train de lancer
        imgs["lance"] = pygame.transform.scale(pygame.image.load(os.path.join(base, f"{p}lance.png")).convert_alpha(),(200, 200))
    except pygame.error as e:  # En cas d'erreur de chargement
        print(f"Err load avatar {avatar_id}({p}):{e}")
        return None
    return imgs


def load_ball_frames(folder, count=15, scale=(90, 100)):
    """
    Charge une séquence d'images (frames) pour l'animation du ballon depuis un dossier spécifié.
    Tente plusieurs conventions de nommage pour les fichiers de frames.
    Les frames sont redimensionnées.

    Args:
        folder (str): Le chemin du dossier contenant les frames du ballon.
        count (int): Le nombre de frames à charger. Par défaut 15.
        scale (tuple): La taille (largeur, hauteur) à laquelle redimensionner les frames. Par défaut (90, 100).

    Returns:
        list: Une liste de surfaces Pygame (les frames du ballon), ou une liste vide en cas d'erreur ou si aucune frame n'est trouvée.
    """
    frames = []  # Liste pour stocker les frames chargées
    if not os.path.isdir(folder):  # Vérifier si le dossier existe
        print(f"Dossier frames balle NI:{folder}")  # NI = Non Identifié
        return frames

    try:
        # Essayer de déduire un préfixe de nom de fichier alternatif à partir du nom du dossier
        # ex: "frames-purple-ball" -> préfixe "purple"
        base_name_parts = folder.split('/')[-1].replace('-ball', '').split('-')
        alt_path_prefix = base_name_parts[-1] if len(base_name_parts) > 0 else "ball"  # Préfixe par défaut "ball"

        for i in range(1, count + 1):  # Boucle pour charger chaque frame (de 1 à `count`)
            # Liste des chemins possibles pour une frame (différentes conventions de nommage)
            possible_paths = [
                os.path.join(folder, f"frame{i}.png"),  # ex: frame1.png
                os.path.join(folder, f"{alt_path_prefix}_{i:02d}.png"),  # ex: purple_01.png
                os.path.join(folder, f"{alt_path_prefix}{i}.png")  # ex: purple1.png
            ]
            path_found = None
            for p_path in possible_paths:  # Essayer chaque chemin possible
                if os.path.exists(p_path):
                    path_found = p_path
                    break  # Arrêter dès qu'un chemin valide est trouvé

            if not path_found:  # Si aucune frame n'est trouvée pour cet index
                print(f"Frame {i} (et alts) manquante dans {folder}.")
                continue  # Passer à la frame suivante

            # Charger, convertir avec alpha, redimensionner et ajouter la frame à la liste
            frames.append(pygame.transform.scale(pygame.image.load(path_found).convert_alpha(), scale))
    except pygame.error as e:  # En cas d'erreur de chargement Pygame
        print(f"Err load frames balle {folder}:{e}")
        return []  # Retourner une liste vide

    if not frames:  # Si aucune frame n'a été chargée
        print(f"Aucune frame chargée pour {folder}")
    return frames


def reset_ball_state(sw, sh):
    """
    Réinitialise l'état du ballon à ses valeurs par défaut (position de départ, pas de tir en cours, etc.).
    La position de départ du ballon est calculée par rapport à la position de l'avatar.

    Args:
        sw (int): Largeur de l'écran.
        sh (int): Hauteur de l'écran.

    Returns:
        dict: Un dictionnaire représentant l'état complet du ballon.
    """
    # Position de l'avatar (coin inférieur gauche)
    avatar_x_pos = 0
    avatar_y_pos = sh - 220  # Ajusté pour que l'avatar soit en bas de l'écran
    avatar_width = 200  # Largeur de l'image de l'avatar (utilisée pour le décalage)

    # Décalages pour positionner le ballon dans la main de l'avatar
    avatar_hand_offset_x = avatar_width * 0.8  # Position X relative à l'avatar
    avatar_hand_offset_y = 50  # Position Y relative au haut de l'avatar

    # Coordonnées de départ réelles du ballon
    actual_start_x = avatar_x_pos + avatar_hand_offset_x
    actual_start_y = avatar_y_pos + avatar_hand_offset_y

    return {
        # Animation du ballon
        "frames": [],  # Liste des frames de l'animation (sera remplie par load_ball_frames)
        "frame_index": 0,  # Index de la frame actuelle
        "frame_delay": 3,  # Nombre de ticks de jeu avant de passer à la frame suivante
        "frame_counter": 0,  # Compteur pour le délai des frames

        # Position et physique du ballon
        "start_x": actual_start_x,  # Position X de départ du tir
        "start_y": actual_start_y,  # Position Y de départ du tir
        "x": actual_start_x,  # Position X actuelle du ballon
        "y": actual_start_y,  # Position Y actuelle du ballon
        "t": 0,  # Temps écoulé depuis le début du tir (pour la physique)
        "angle": math.radians(60),  # Angle de tir initial en radians (60 degrés)
        "velocity": 7,  # Vélocité initiale du tir
        "gravity": 0.03,  # Constante de gravité affectant le ballon

        # État du tir
        "shooting": False,  # True si le ballon est en cours de tir
        "animation_done": False,  # (Non utilisé actuellement) Pourrait indiquer la fin de l'animation de lancer

        # Position de l'avatar (pour le dessin)
        "x_avatar": avatar_x_pos,
        "y_avatar": avatar_y_pos,

        # État du score pour ce tir
        "scored_this_throw": False,  # True si le ballon a marqué un panier lors de ce tir
        "vy_physics": 0  # Composante verticale de la vitesse (utilisée pour la détection de panier)
    }


def update_ball(s, sw, sh, folder_unused):
    """
    Met à jour l'état du ballon à chaque tick de jeu.
    Gère l'animation du ballon et sa trajectoire physique s'il est en train d'être tiré.
    Réinitialise le ballon s'il sort de l'écran.

    Args:
        s (dict): L'état actuel du ballon.
        sw (int): Largeur de l'écran.
        sh (int): Hauteur de l'écran.
        folder_unused (str): Prévu pour le chemin des frames, mais les frames sont déjà dans `s["frames"]`.
    """
    # Si le ballon n'est pas en train d'être tiré, ou si l'animation de tir est terminée (non utilisé)
    # le ballon reste à sa position de départ.
    if not s["shooting"] or s.get("animation_done", False):
        if not s["shooting"]:  # Si pas en tir, s'assurer que le ballon est à la position de départ
            s["x"] = s["start_x"]
            s["y"] = s["start_y"]
            s["frame_index"] = 0
        return  # Pas d'autre mise à jour nécessaire

    # --- Animation du ballon ---
    s["frame_counter"] += 1
    if s["frames"] and len(s["frames"]) > 0:  # S'il y a des frames chargées
        if s["frame_counter"] >= s["frame_delay"]:  # Si le délai est atteint
            s["frame_counter"] = 0  # Réinitialiser le compteur
            s["frame_index"] = (s["frame_index"] + 1) % len(s["frames"])  # Passer à la frame suivante (boucle)
    else:  # S'il n'y a pas de frames, l'index reste à 0
        s["frame_index"] = 0

    # --- Physique du ballon (trajectoire parabolique) ---
    s["t"] += 1  # Incrémenter le temps écoulé depuis le lancer

    # Calcul de la position X (mouvement horizontal uniforme)
    s["x"] = s["start_x"] + s["velocity"] * s["t"] * math.cos(s["angle"])

    # Calcul de la position Y (mouvement vertical affecté par la gravité)
    # Formule: y(t) = y0 - (v0y * t - 0.5 * g * t^2)  (l'axe Y est inversé dans Pygame, d'où le signe)
    # Ici, g est 2 * s["gravity"] car on utilise s["gravity"] * t^2 au lieu de 0.5 * g_physique * t^2
    term_vy = s["velocity"] * s["t"] * math.sin(s["angle"])  # Composante verticale de la vitesse * temps
    term_g = s["gravity"] * s["t"] ** 2  # Effet de la gravité
    s["y"] = s["start_y"] - (term_vy - term_g)

    # Calcul de la composante verticale de la vitesse actuelle (vy_physics)
    # v_y(t) = v0y - g * t
    v0y = s["velocity"] * math.sin(s["angle"]) # Vitesse verticale initiale
    s["vy_physics"] = v0y - 2 * s["gravity"] * s["t"]  # La vitesse verticale actuelle (2*gravity car g=0.5*g_physique)
    # Utile pour savoir si le ballon monte ou descend.

    # --- Réinitialisation du ballon s'il sort de l'écran ---
    bw = s["frames"][0].get_width() if s["frames"] else 0  # Largeur du ballon (pour les limites)
    # Si le ballon sort largement des limites de l'écran
    if s["x"] > sw + bw or s["y"] > sh + bw:
        # Condition additionnelle pour éviter une réinitialisation prématurée si le ballon monte très haut hors écran
        # mais va retomber (vy_physics > 0.05 signifie qu'il monte encore significativement)
        if not (s["y"] < -sh * 1.5 and s["vy_physics"] > 0.05):
            # Sauvegarder les frames, l'angle et la vélocité actuels (pour les conserver pour le prochain tir)
            cf = s["frames"]
            ca = s["angle"]
            cv = s["velocity"]
            # Réinitialiser l'état du ballon
            nbs = reset_ball_state(sw, sh)
            s.clear()
            s.update(nbs)
            # Restaurer les frames, l'angle et la vélocité
            s["frames"] = cf
            s["angle"] = ca
            s["velocity"] = cv


def draw_ball(surf, s, avatar_imgs):
    """
    Dessine l'avatar et le ballon sur la surface donnée.

    Args:
        surf (pygame.Surface): La surface sur laquelle dessiner.
        s (dict): L'état actuel du ballon (contient aussi la position de l'avatar et l'état de tir).
        avatar_imgs (dict): Un dictionnaire contenant les images de l'avatar ("side", "lance").
    """
    # --- Dessin de l'avatar ---
    if avatar_imgs:
        # Choisir l'image de l'avatar en fonction de l'état de tir
        img = avatar_imgs.get("lance") if s["shooting"] else avatar_imgs.get("side")
        # Fallback si une image spécifique manque
        if not img: img = avatar_imgs.get("lance", avatar_imgs.get("side"))
        if img: surf.blit(img, (s["x_avatar"], s["y_avatar"]))  # Dessiner l'avatar

    # --- Dessin du ballon ---
    if s["frames"] and len(s["frames"]) > 0:  # S'il y a des frames chargées
        # S'assurer que l'index de la frame est valide
        idx = s["frame_index"] % len(s["frames"])
        surf.blit(s["frames"][idx], (s["x"], s["y"]))  # Dessiner la frame actuelle du ballon


def launch_ball(s):
    """
    Initialise le processus de tir du ballon.
    Met l'état "shooting" à True et réinitialise les variables de physique du tir.

    Args:
        s (dict): L'état actuel du ballon.
    """
    if not s["shooting"]:  # Ne lancer que si le ballon n'est pas déjà en tir
        s["shooting"] = True  # Mettre en mode tir
        s["t"] = 0  # Réinitialiser le temps du tir
        s["x"] = s["start_x"]  # Commencer à la position de départ X
        s["y"] = s["start_y"]  # Commencer à la position de départ Y
        s["animation_done"] = False  # (Non utilisé)
        s["frame_index"] = 0  # Commencer l'animation à la première frame
        s["scored_this_throw"] = False  # Réinitialiser le statut de score pour ce tir
        s["vy_physics"] = s["velocity"] * math.sin(s["angle"])  # Vitesse verticale initiale pour ce tir


def adjust_ball_angle(s, d):
    """
    Ajuste l'angle de tir du ballon (si le ballon n'est pas en cours de tir).

    Args:
        s (dict): L'état actuel du ballon.
        d (str): La direction de l'ajustement ("up" ou "down").
    """
    if s["shooting"]: return  # Ne pas ajuster si le ballon est déjà en l'air

    deg = math.degrees(s["angle"])  # Convertir l'angle actuel en degrés
    if d == "up" and deg < 85:
        deg += 2  # Augmenter l'angle (max 85 degrés)
    elif d == "down" and deg > 30:
        deg -= 2  # Diminuer l'angle (min 30 degrés)
    s["angle"] = math.radians(deg)  # Reconvertir en radians et sauvegarder


def adjust_ball_velocity(s, d):
    """
    Ajuste la puissance de tir du ballon.

    Args:
        s (dict): L'état actuel du ballon.
        d (str): La direction de l'ajustement ("right" pour augmenter, "left" pour diminuer).
    """
    if s["shooting"]: return  # Ne pas ajuster si le ballon est déjà en l'air

    min_vo = 1
    max_vo = 15
    inc = 0.5  # Limites min/max et incrément de la vélocité
    if d == "right" and s["velocity"] < max_vo:
        s["velocity"] += inc  # Augmenter la vélocité
    elif d == "left" and s["velocity"] > min_vo:
        s["velocity"] -= inc  # Diminuer la vélocité


def draw_trajectory_dots(surf, s, sw, sh, hoop_info=None):
    """
    Dessine une prévisualisation de la trajectoire du ballon sous forme de points.

    Args:
        surf (pygame.Surface): La surface sur laquelle dessiner les points.
        s (dict): L'état actuel du ballon (pour obtenir les paramètres de tir).
        sw (int): Largeur de l'écran.
        sh (int): Hauteur de l'écran.
        hoop_info (dict, optional): Informations sur le rectangle du panier {"x", "y", "width", "height"}. Par défaut None.
    """
    if s["shooting"]: return  # Ne pas dessiner la trajectoire si le ballon est en l'air

    dot_col = (255, 255, 255)  # Couleur des points de trajectoire (blanc)
    hoop_rect = None
    if hoop_info:  # Si les informations du panier sont fournies, créer un rectangle de collision
        hoop_rect = pygame.Rect(hoop_info["x"], hoop_info["y"], hoop_info["width"], hoop_info["height"])

    step_t = 2  # Intervalle de temps entre les points simulés
    max_t_pred = 120  # Temps maximum de simulation pour la trajectoire

    for td_sim in range(step_t, max_t_pred, step_t):  # Simuler la trajectoire par pas de temps
        # Calculer la position (xd, yd) du ballon au temps simulé `td_sim`
        xd = s["start_x"] + s["velocity"] * td_sim * math.cos(s["angle"])
        term_vy_p = s["velocity"] * td_sim * math.sin(s["angle"])
        term_g_p = s["gravity"] * td_sim ** 2
        yd = s["start_y"] - (term_vy_p - term_g_p)

        # Calculer la vitesse verticale au temps simulé
        v0y_p = s["velocity"] * math.sin(s["angle"])
        vy_p_phys = v0y_p - 2 * s["gravity"] * td_sim

        # Si un panier est défini, vérifier si le point simulé entre en collision avec
        if hoop_rect:
            dot_center = (int(xd), int(yd))
            # Si le point entre en collision avec le panier ET que le ballon descend (vy_p_phys < 0)
            if hoop_rect.collidepoint(dot_center) and vy_p_phys < 0:
                # Mettre en évidence ce point et quelques points suivants pour montrer le passage à travers le panier
                for k_off_f in range(5):  # Dessiner 5 points supplémentaires
                    td_ex = td_sim + k_off_f * step_t
                    if td_ex >= max_t_pred: break  # Ne pas dépasser le temps max de simulation

                    # Recalculer la position pour ces points supplémentaires
                    xd_ex = s["start_x"] + s["velocity"] * td_ex * math.cos(s["angle"])
                    term_vy_ex = s["velocity"] * td_ex * math.sin(s["angle"])
                    term_g_ex = s["gravity"] * td_ex ** 2
                    yd_ex = s["start_y"] - (term_vy_ex - term_g_ex)

                    # Dessiner ces points s'ils sont dans des limites d'écran raisonnables
                    if -sw * 0.5 < xd_ex < sw * 1.5 and -sh * 2 < yd_ex < sh * 1.5:
                        pygame.draw.circle(surf, dot_col, (int(xd_ex), int(yd_ex)),
                                           5)  # Points plus gros ou couleur différente?
                break  # Arrêter de dessiner d'autres points de trajectoire si le panier est touché

        # Définir des marges pour ne pas dessiner des points trop loin hors de l'écran
        draw_marg_yt = sh * 2  # Marge verticale (peut aller très haut)
        draw_marg_xs = sw * 0.75  # Marge horizontale

        # Si le point simulé est trop loin hors de l'écran, ne pas le dessiner
        if xd < -draw_marg_xs or xd > sw + draw_marg_xs or yd > sh + 100 or yd < -draw_marg_yt:
            # Condition spéciale pour arrêter tôt si le ballon tombe loin en dessous sans avoir touché le panier
            if yd > sh + 150 and vy_p_phys < 0: break
            continue  # Passer au point suivant

        # Dessiner le point de trajectoire normal
        pygame.draw.circle(surf, dot_col, (int(xd), int(yd)), 5)  # Rayon de 5 pixels