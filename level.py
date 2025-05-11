# level.py
# Gère tout ce qui concerne le panier de basket : son image, sa position, ses mouvements en fonction de la difficulté et du niveau, ainsi que les limites de déplacement.

import pygame
import math

# --- Chargement de l'image du panier ---
basket_img_original_raw = pygame.image.load("image/basket.png")
basket_img_scaled = None  # Variable pour stocker l'image du panier redimensionnée et convertie

# --- Définition des difficultés et états du panier ---
difficulty = ["Easy", "Normal", "Intermediate", "Difficult"]  # Noms des paliers de difficulté
_basket_x = 900  # Position X initiale du panier
_basket_y = 175  # Position Y initiale du panier
_basket_direction_x = 1  # Direction de mouvement horizontal du panier (1: droite, -1: gauche)
_basket_direction_y = 1  # Direction de mouvement vertical du panier (1: bas, -1: haut)
_basket_state_machine = "right"  # État pour les mouvements complexes (ex: carré, T, hexagone)

# --- Constantes pour les dimensions et marges ---
BASKET_WIDTH = 200  # Largeur du panier
BASKET_HEIGHT = 175  # Hauteur du panier
MARGIN = 20  # Marge par rapport aux bords de l'écran pour le mouvement du panier

# --- Limites de la zone de mouvement du panier ---
# Ces variables seront calculées dans en fonction de la taille de l'écran.
H_LIMIT_LEFT_ZONE = 0  # Limite gauche de la zone de déplacement horizontal
H_LIMIT_RIGHT_ZONE = 0  # Limite droite
V_LIMIT_TOP_ZONE = 0  # Limite haute de la zone de déplacement vertical
V_LIMIT_BOTTOM_ZONE = 0  # Limite basse

# --- Points de chemin prédéfinis pour les mouvements complexes (difficultés "Intermediate" et "Difficult") ---

# Points pour un mouvement carré
SQUARE_TL_R, SQUARE_TR_R, SQUARE_BR_R, SQUARE_BL_R = (0, 0), (0, 0), (0, 0), (0, 0)  # Top-Left, Top-Right, etc.

# Points pour un mouvement en "T"
T_TOP_L_R, T_TOP_R_R, T_STEM_TOP_R, T_STEM_BOTTOM_R = (0, 0), (0, 0), (0, 0), (0, 0)  # Barre horizontale et tige verticale

# Points pour un mouvement triangulaire
TRI_PT_TOP_R, TRI_PT_LEFT_R, TRI_PT_RIGHT_R = (0, 0), (0, 0), (0, 0)  # Sommets du triangle

# Points pour un mouvement hexagonal
HEX_P1_R, HEX_P2_R, HEX_P3_R, HEX_P4_R, HEX_P5_R, HEX_P6_R = [(0, 0)] * 6  # 6 sommets de l'hexagone


def init_level_assets(sw_param, sh_param):
    """
    Initialise les assets et paramètres du niveau.
    - Redimensionne et convertit l'image du panier.
    - Met à jour les dimensions globales du panier.
    - Calcule les limites de la zone de mouvement du panier.
    - Calcule les coordonnées des points de chemin pour les mouvements complexes.

    Args:
        sw_param (int): Largeur de l'écran.
        sh_param (int): Hauteur de l'écran.
    """
    global basket_img_scaled, BASKET_WIDTH, BASKET_HEIGHT
    global H_LIMIT_LEFT_ZONE, H_LIMIT_RIGHT_ZONE, V_LIMIT_TOP_ZONE, V_LIMIT_BOTTOM_ZONE
    global SQUARE_TL_R, SQUARE_TR_R, SQUARE_BR_R, SQUARE_BL_R
    global T_TOP_L_R, T_TOP_R_R, T_STEM_TOP_R, T_STEM_BOTTOM_R
    global TRI_PT_TOP_R, TRI_PT_LEFT_R, TRI_PT_RIGHT_R
    global HEX_P1_R, HEX_P2_R, HEX_P3_R, HEX_P4_R, HEX_P5_R, HEX_P6_R

    # Convertir l'image originale du panier avec gestion de la transparence alpha
    basket_img_original_converted = basket_img_original_raw.convert_alpha()
    # Redimensionner et lisse l'image du panier
    basket_img_scaled = pygame.transform.smoothscale(basket_img_original_converted, (200, 175))
    # Mettre à jour les dimensions globales du panier avec celles de l'image redimensionnée
    BASKET_WIDTH = basket_img_scaled.get_width()
    BASKET_HEIGHT = basket_img_scaled.get_height()

    # Calcul des limites de la zone de mouvement du panier
    H_LIMIT_LEFT_ZONE = sw_param / 2 + MARGIN  # Commence à partir du milieu de l'écran plus une marge
    H_LIMIT_RIGHT_ZONE = sw_param - BASKET_WIDTH - MARGIN  # Se termine avant le bord droit moins la largeur du panier et une marge
    V_LIMIT_TOP_ZONE = MARGIN + 50  # Marge en haut, plus un espace pour le score et le temps
    V_LIMIT_BOTTOM_ZONE = sh_param - BASKET_HEIGHT - MARGIN - 50  # Marge en bas, moins hauteur panier et espace pour le bouton quit

    # --- Calcul des points de chemin pour les mouvements complexes ---

    # Mouvement carré
    square_size = 150  # Taille du côté du carré
    SQUARE_TL_R = (H_LIMIT_LEFT_ZONE + 50, V_LIMIT_TOP_ZONE + 50)  # Point de départ (en haut à gauche du carré)
    SQUARE_TR_R = (SQUARE_TL_R[0] + square_size, SQUARE_TL_R[1])
    SQUARE_BR_R = (SQUARE_TR_R[0], SQUARE_TR_R[1] + square_size)
    SQUARE_BL_R = (SQUARE_TL_R[0], SQUARE_BR_R[1])

    # Mouvement en "T"
    t_bar_width = 200  # Largeur de la barre horizontale du T
    t_stem_height = 150  # Hauteur de la tige verticale du T
    # Centre la barre du T horizontalement dans la zone de mouvement
    T_TOP_L_R = ((H_LIMIT_LEFT_ZONE + H_LIMIT_RIGHT_ZONE - t_bar_width) // 2, V_LIMIT_TOP_ZONE + 50)
    T_TOP_R_R = (T_TOP_L_R[0] + t_bar_width, T_TOP_L_R[1])
    T_STEM_TOP_R = (T_TOP_L_R[0] + t_bar_width // 2, T_TOP_L_R[1])  # Haut de la tige (milieu de la barre)
    T_STEM_BOTTOM_R = (T_STEM_TOP_R[0], T_STEM_TOP_R[1] + t_stem_height)  # Bas de la tige

    # Mouvement triangulaire
    tri_base_width = 200  # Largeur de la base du triangle
    tri_height = 150  # Hauteur du triangle
    TRI_PT_TOP_R = ((H_LIMIT_LEFT_ZONE + H_LIMIT_RIGHT_ZONE) // 2, V_LIMIT_TOP_ZONE + 30)  # Sommet supérieur, centré
    TRI_PT_LEFT_R = (TRI_PT_TOP_R[0] - tri_base_width // 2, TRI_PT_TOP_R[1] + tri_height)  # Coin inférieur gauche
    TRI_PT_RIGHT_R = (TRI_PT_TOP_R[0] + tri_base_width // 2, TRI_PT_TOP_R[1] + tri_height)  # Coin inférieur droit

    # Mouvement hexagonal
    hex_radius = 80  # Rayon du cercle circonscrit à l'hexagone
    # Centre de l'hexagone au centre de la zone de mouvement
    hex_center_x_zone = (H_LIMIT_LEFT_ZONE + H_LIMIT_RIGHT_ZONE) // 2
    hex_center_y_zone = (V_LIMIT_TOP_ZONE + V_LIMIT_BOTTOM_ZONE) // 2
    # Calcul des 6 sommets de l'hexagone
    HEX_P1_R = (hex_center_x_zone - hex_radius // 2, hex_center_y_zone - int(hex_radius * math.sqrt(3) / 2))
    HEX_P2_R = (hex_center_x_zone + hex_radius // 2, hex_center_y_zone - int(hex_radius * math.sqrt(3) / 2))
    HEX_P3_R = (hex_center_x_zone + hex_radius, hex_center_y_zone)
    HEX_P4_R = (hex_center_x_zone + hex_radius // 2, hex_center_y_zone + int(hex_radius * math.sqrt(3) / 2))
    HEX_P5_R = (hex_center_x_zone - hex_radius // 2, hex_center_y_zone + int(hex_radius * math.sqrt(3) / 2))
    HEX_P6_R = (hex_center_x_zone - hex_radius, hex_center_y_zone)


def get_basket_rect():
    """
    Retourne le rectangle du panier
    Returns:
        pygame.Rect: Le rectangle de l'image du panier, ou un rectangle vide si non chargée.
    """
    if basket_img_scaled:
        return basket_img_scaled.get_rect()
    return pygame.Rect(0, 0, 0, 0)  # Rectangle vide par défaut


def reset_basket_position_for_level(diff_sel_idx, lvl_val, SW_UNUSED, SH_UNUSED):
    """
    Réinitialise la position de départ et l'état de mouvement du panier en fonction de la difficulté et du niveau sélectionnés.

    Args:
        diff_sel_idx (int): Index de la difficulté sélectionnée.
        lvl_val (int): Index du niveau actuel dans cette difficulté.
        SW_UNUSED, SH_UNUSED: Largeur et hauteur de l'écran (non utilisées directement ici, car les limites sont déjà calculées).
    """
    global _basket_x, _basket_y, _basket_direction_x, _basket_direction_y, _basket_state_machine

    diff_name = difficulty[diff_sel_idx]  # Nom de la difficulté

    # Position et direction par défaut (sera souvent écrasée)
    _basket_x = H_LIMIT_LEFT_ZONE
    _basket_y = V_LIMIT_TOP_ZONE + (V_LIMIT_BOTTOM_ZONE - V_LIMIT_TOP_ZONE) // 2  # Centré verticalement
    _basket_direction_x = 1  # Mouvement vers la droite
    _basket_direction_y = 1  # Mouvement vers le bas

    if diff_name == "Easy":
        # Panier fixe au centre horizontalement, en haut de la zone
        _basket_x = (H_LIMIT_LEFT_ZONE + H_LIMIT_RIGHT_ZONE) // 2
        _basket_y = V_LIMIT_TOP_ZONE + 50
    elif diff_name == "Normal" or diff_name == "Intermediate":
        if lvl_val == 0:  # Mouvement horizontal simple
            _basket_x = H_LIMIT_LEFT_ZONE
            _basket_state_machine = "right"  # Commence à gauche, va vers la droite
        elif lvl_val == 1:  # Mouvement vertical simple
            _basket_y = V_LIMIT_TOP_ZONE
            _basket_state_machine = "down"  # Commence en haut, va vers le bas
        elif lvl_val == 2:  # Mouvement carré (pour "Intermediate", Normal n'a que 2 niveaux de base)
            _basket_x, _basket_y = SQUARE_TL_R
            _basket_state_machine = "square_R_to_TR"  # Commence au coin du carré
    elif diff_name == "Difficult":
        if lvl_val == 0:  # Mouvement en "T"
            _basket_x, _basket_y = T_TOP_L_R
            _basket_state_machine = "t_R_bar_right"
        elif lvl_val == 1:  # Mouvement diagonal
            _basket_x = H_LIMIT_LEFT_ZONE
            _basket_y = V_LIMIT_TOP_ZONE
            _basket_state_machine = "diag_R_down_right"
        elif lvl_val == 2:  # Mouvement triangulaire
            _basket_x, _basket_y = TRI_PT_TOP_R
            _basket_state_machine = "tri_R_to_left_bottom"
        elif lvl_val == 3:  # Mouvement carré (plus rapide qu'en Intermediate)
            _basket_x, _basket_y = SQUARE_TL_R
            _basket_state_machine = "square_R_to_TR"
        elif lvl_val == 4:  # Mouvement hexagonal
            _basket_x, _basket_y = HEX_P1_R
            _basket_state_machine = "hex_R_to_p2"


def move_towards_target(cur, tar, spd):
    """
    Calcule la nouvelle position pour un mouvement d'un point `cur` vers un point `tar` à une vitesse `spd`.

    Args:
        cur (tuple): Coordonnées (x, y) actuelles.
        tar (tuple): Coordonnées (x, y) cibles.
        spd (float): Vitesse de déplacement.

    Returns:
        tuple: (nouvelle_position, a_atteint_la_cible)
               - nouvelle_position (tuple): Les nouvelles coordonnées (x, y).
               - a_atteint_la_cible (bool): True si la cible est atteinte ou dépassée, False sinon.
    """
    dx = tar[0] - cur[0]  # Différence en x
    dy = tar[1] - cur[1]  # Différence en y
    dist = math.sqrt(dx ** 2 + dy ** 2)  # Distance à la cible

    # Si la distance est inférieure à la vitesse considérer la cible comme atteinte.
    if dist < spd * 1.1:
        return tar, True  # Se positionner directement sur la cible

    # Calculer le déplacement unitaire et le multiplier par la vitesse
    return (cur[0] + (dx / dist) * spd, cur[1] + (dy / dist) * spd), False


def basket_hoop(screen_surface, cur_diff_sel, cur_lvl, SW_UNUSED, SH_UNUSED):
    """
    Gère le mouvement et l'affichage du panier.
    La logique de mouvement dépend de la difficulté et du niveau actuels.

    Args:
        screen_surface (pygame.Surface): La surface sur laquelle dessiner le panier.
        cur_diff_sel (int): Index de la difficulté actuelle.
        cur_lvl (int): Index du niveau actuel.
        SW_UNUSED, SH_UNUSED: Largeur/hauteur de l'écran (non utilisées directement pour le mouvement car les limites sont globales).

    Returns:
        tuple: (x, y) de la position actuelle du panier après mouvement.
    """
    global _basket_x, _basket_y, _basket_direction_x, _basket_direction_y, _basket_state_machine

    if not basket_img_scaled:
        return _basket_x, _basket_y  # Si l'image n'est pas chargée, ne rien faire

    diff_name = difficulty[cur_diff_sel]  # Nom de la difficulté
    lvl = cur_lvl  # Niveau actuel

    # Détermination de la vitesse du panier en fonction de la difficulté
    speed = 0
    if diff_name == "Easy":
        speed = 0  # Panier immobile
    elif diff_name == "Normal":
        speed = 1.8
    elif diff_name == "Intermediate":
        speed = 3.0
    elif diff_name == "Difficult":
        speed = 4.0

    # Récupération des limites de mouvement pour la lisibilité
    h_lim_l, h_lim_r = H_LIMIT_LEFT_ZONE, H_LIMIT_RIGHT_ZONE
    v_lim_t, v_lim_b = V_LIMIT_TOP_ZONE, V_LIMIT_BOTTOM_ZONE

    # --- Logique de mouvement spécifique à la difficulté et au niveau ---
    if diff_name == "Easy":
        pass  # Le panier est fixe, positionné par reset_basket_position_for_level

    elif diff_name == "Normal" or diff_name == "Intermediate":
        if lvl == 0:  # Mouvement horizontal simple
            _basket_x += _basket_direction_x * speed
            if (_basket_direction_x == 1 and _basket_x >= h_lim_r) or (_basket_direction_x == -1 and _basket_x <= h_lim_l):
                _basket_direction_x *= -1  # Inverser la direction en atteignant une limite
                _basket_x = max(h_lim_l, min(_basket_x, h_lim_r))  # S'assurer de rester dans les limites
        elif lvl == 1:  # Mouvement vertical simple
            _basket_y += _basket_direction_y * speed
            if (_basket_direction_y == 1 and _basket_y >= v_lim_b) or (_basket_direction_y == -1 and _basket_y <= v_lim_t):
                _basket_direction_y *= -1
                _basket_y = max(v_lim_t, min(_basket_y, v_lim_b))
        elif lvl == 2:  # Mouvement carré (pour "Intermediate")
            target_pos = (_basket_x, _basket_y)  # Position cible par défaut
            next_s_state = _basket_state_machine  # Prochain état de la machine d'état
            # Déterminer la cible et le prochain état en fonction de l'état actuel
            if _basket_state_machine == "square_R_to_TR":
                target_pos = SQUARE_TR_R; next_s_state = "square_R_to_BR"
            elif _basket_state_machine == "square_R_to_BR":
                target_pos = SQUARE_BR_R; next_s_state = "square_R_to_BL"
            elif _basket_state_machine == "square_R_to_BL":
                target_pos = SQUARE_BL_R; next_s_state = "square_R_to_TL"
            elif _basket_state_machine == "square_R_to_TL":
                target_pos = SQUARE_TL_R; next_s_state = "square_R_to_TR"

            new_pos, reached = move_towards_target((_basket_x, _basket_y), target_pos, speed)
            _basket_x, _basket_y = new_pos
            if reached:
                _basket_state_machine = next_s_state  # Passer à l'état suivant si la cible est atteinte

    elif diff_name == "Difficult":
        cur_p = (_basket_x, _basket_y)  # Position actuelle
        tar_p = cur_p  # Position cible
        next_s = _basket_state_machine  # Prochain état

        if lvl == 0:  # Mouvement en "T"
            if _basket_state_machine == "t_R_bar_right":
                tar_p = T_TOP_R_R; next_s = "t_R_bar_left_then_stem"
            elif _basket_state_machine == "t_R_bar_left_then_stem":
                tar_p = T_TOP_L_R; next_s = "t_R_stem_down"
            elif _basket_state_machine == "t_R_stem_down":
                tar_p = T_STEM_BOTTOM_R; next_s = "t_R_stem_up_then_bar"
            elif _basket_state_machine == "t_R_stem_up_then_bar":
                tar_p = T_STEM_TOP_R; next_s = "t_R_bar_right"
        elif lvl == 1:  # Mouvement diagonal
            tdr = (H_LIMIT_RIGHT_ZONE, V_LIMIT_BOTTOM_ZONE)  # Cible en bas à droite
            tul = (H_LIMIT_LEFT_ZONE, V_LIMIT_TOP_ZONE)  # Cible en haut à gauche
            if _basket_state_machine == "diag_R_down_right":
                tar_p = tdr; next_s = "diag_R_up_left"
            elif _basket_state_machine == "diag_R_up_left":
                tar_p = tul; next_s = "diag_R_down_right"
        elif lvl == 2:  # Mouvement triangulaire
            if _basket_state_machine == "tri_R_to_left_bottom":
                tar_p = TRI_PT_LEFT_R; next_s = "tri_R_to_right_bottom"
            elif _basket_state_machine == "tri_R_to_right_bottom":
                tar_p = TRI_PT_RIGHT_R; next_s = "tri_R_to_top"
            elif _basket_state_machine == "tri_R_to_top":
                tar_p = TRI_PT_TOP_R; next_s = "tri_R_to_left_bottom"
        elif lvl == 3:  # Mouvement carré (identique à Intermediate lvl 2, mais plus rapide)
            if _basket_state_machine == "square_R_to_TR":
                tar_p = SQUARE_TR_R; next_s = "square_R_to_BR"
            # (autres états du carré)
            elif _basket_state_machine == "square_R_to_BR":
                tar_p = SQUARE_BR_R;next_s = "square_R_to_BL"
            elif _basket_state_machine == "square_R_to_BL":
                tar_p = SQUARE_BL_R;next_s = "square_R_to_TL"
            elif _basket_state_machine == "square_R_to_TL":
                tar_p = SQUARE_TL_R;next_s = "square_R_to_TR"
        elif lvl == 4:  # Mouvement hexagonal
            if _basket_state_machine == "hex_R_to_p2":
                tar_p = HEX_P2_R; next_s = "hex_R_to_p3"
            elif _basket_state_machine == "hex_R_to_p3":
                tar_p = HEX_P3_R; next_s = "hex_R_to_p4"
            elif _basket_state_machine == "hex_R_to_p4":
                tar_p = HEX_P4_R; next_s = "hex_R_to_p5"
            elif _basket_state_machine == "hex_R_to_p5":
                tar_p = HEX_P5_R; next_s = "hex_R_to_p6"
            elif _basket_state_machine == "hex_R_to_p6":
                tar_p = HEX_P6_R; next_s = "hex_R_to_p1"
            elif _basket_state_machine == "hex_R_to_p1":
                tar_p = HEX_P1_R; next_s = "hex_R_to_p2"

        # Appliquer le mouvement vers la cible déterminée
        new_p, reached = move_towards_target(cur_p, tar_p, speed)
        _basket_x, _basket_y = new_p
        if reached:
            _basket_state_machine = next_s  # Passer à l'état suivant

    # S'assurer que le panier reste dans les limites de la zone de mouvement après toutes les mises à jour
    _basket_x = max(H_LIMIT_LEFT_ZONE, min(_basket_x, H_LIMIT_RIGHT_ZONE))
    _basket_y = max(V_LIMIT_TOP_ZONE, min(_basket_y, V_LIMIT_BOTTOM_ZONE))

    # Afficher l'image du panier à sa nouvelle position
    screen_surface.blit(basket_img_scaled, (_basket_x, _basket_y))

    return _basket_x, _basket_y