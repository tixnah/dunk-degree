# sound_manager.py
# Gère la lecture de la musique de fond dans le jeu.
# Permet de jouer, arrêter, mettre en fondu, et vérifier l'état de la musique.

import pygame
import os

# Dictionnaire associant des clés de musique à leurs chemins de fichier.
music_paths = {
    "menu": "sound/menu.mp3",  # Musique du menu principal
    "palier1_easy": "sound/palier1_easy.mp3",  # Musique pour la difficulté Facile
    "palier2_normal": "sound/palier2_normal.mp3",  # Musique pour la difficulté Normale
    "palier3_intermediate": "sound/palier3_intermediate.mp3",  # Musique pour la difficulté Intermédiaire
    "palier4_difficult": "sound/palier4_difficult.mp3",  # Musique pour la difficulté Difficile
    "score_fin_win": "sound/end_music.mp3",  # Musique de victoire (fin de jeu)
    "game_over_lose": "sound/end_music.mp3"  # Musique de défaite (game over) - utilise la même que la victoire pour l'instant
}
# Variable pour stocker la clé de la musique actuellement jouée.
current_music_key = None


def init_mixer():
    """
    Initialise le module `pygame.mixer` s'il ne l'est pas déjà.
    """
    if not pygame.mixer.get_init():  # Vérifie si le mixer est déjà initialisé
        try:
            pygame.mixer.init()  # Initialise le mixer
        except pygame.error as e:
            print(f"Erreur init mixer: {e}")  # Affiche une erreur si l'initialisation échoue


def play_music(key, loops=-1, volume=0.5, fade_ms=1000):
    """
    Joue une musique identifiée par sa clé.
    Gère le fondu enchaîné si une autre musique est déjà en cours.

    Args:
        key (str): La clé de la musique à jouer (doit exister dans `music_paths`).
        loops (int): Nombre de répétitions. -1 pour infini. Par défaut -1.
        volume (float): Volume de la musique (entre 0.0 et 1.0). Par défaut 0.5.
        fade_ms (int): Durée du fondu en millisecondes pour la musique précédente. Par défaut 1000 ms.
    """
    global current_music_key
    init_mixer()  # S'assurer que le mixer est initialisé
    if not pygame.mixer.get_init():
        return  # Quitter si le mixer n'a pas pu être initialisé

    # Vérifier si la clé de musique est valide
    if key not in music_paths:
        print(f"Err: Clé musique '{key}' NI.")  # NI = Non Identifiée/Non Incluse
        return
    music_file = music_paths[key]  # Obtenir le chemin du fichier musical

    # Vérifier si le fichier musical existe
    if not os.path.exists(music_file):
        print(f"Err: Fichier musical NI : {music_file}")
        return

    try:
        # Si la même musique est demandée et qu'elle est déjà en cours, ne rien faire
        if current_music_key == key and pygame.mixer.music.get_busy():
            return

        # Si une autre musique est en cours, l'arrêter avec un fondu
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)  # Fondu sortant
            pygame.time.wait(
                fade_ms)  # Attendre la fin du fondu (bloquant, mais pour la musique c'est souvent acceptable)
            pygame.mixer.music.stop()  # Arrêter explicitement
            pygame.mixer.music.unload()  # Décharger la musique précédente

        # Charger et jouer la nouvelle musique
        pygame.mixer.music.load(music_file)  # Charger le fichier
        pygame.mixer.music.set_volume(volume)  # Définir le volume
        pygame.mixer.music.play(loops)  # Jouer la musique
        current_music_key = key  # Mettre à jour la clé de la musique actuelle
    except pygame.error as e:
        print(f"Err lecture/chargement musique {music_file}: {e}");
        current_music_key = None  # Réinitialiser en cas d'erreur


def stop_music():
    """
    Arrête la musique actuellement jouée et la décharge.
    """
    global current_music_key
    init_mixer()  # S'assurer que le mixer est initialisé
    if not pygame.mixer.get_init(): return

    pygame.mixer.music.stop()  # Arrêter la musique
    pygame.mixer.music.unload()  # Décharger la musique de la mémoire
    current_music_key = None  # Aucune musique n'est plus en cours


def fadeout_music(time_ms):
    """
    Effectue un fondu sortant sur la musique actuellement jouée.
    La musique s'arrêtera après le fondu.

    Args:
        time_ms (int): Durée du fondu en millisecondes.
    """
    init_mixer()
    if not pygame.mixer.get_init(): return
    pygame.mixer.music.fadeout(time_ms)

def set_volume(volume):
    """
    Définit le volume de la musique.

    Args:
        volume (float): Le nouveau volume (entre 0.0 et 1.0).
    """
    init_mixer()
    if not pygame.mixer.get_init():
        return

    if 0.0 <= volume <= 1.0:  # Vérifier que le volume est dans la plage valide
        pygame.mixer.music.set_volume(volume)
    else:
        print("Volume invalide.")


def is_playing(key=None):
    """
    Vérifie si une musique est en cours de lecture.
    Si une clé est fournie, vérifie si CETTE musique spécifique est en cours.

    Args:
        key (str, optional): La clé de la musique à vérifier. Par défaut None.

    Returns:
        bool: True si la musique est en cours, False sinon.
    """
    init_mixer()
    if not pygame.mixer.get_init():
        return False  # Pas de musique si le mixer n'est pas initialisé

    if key:  # Si une clé spécifique est demandée
        return pygame.mixer.music.get_busy() and current_music_key == key
    # Sinon, vérifier si n'importe quelle musique est en cours
    return pygame.mixer.music.get_busy()