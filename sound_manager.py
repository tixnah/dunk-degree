# sound_manager.py
import pygame
import os

music_paths = {
    "menu": "sound/menu.mp3",
    "palier1_easy": "sound/palier1_easy.mp3",
    "palier2_normal": "sound/palier2_normal.mp3",
    "palier3_intermediate": "sound/palier3_intermediate.mp3",
    "palier4_difficult": "sound/palier4_difficult.mp3",
    "score_fin_win": "sound/end_music.mp3",
    "game_over_lose": "sound/end_music.mp3"
}
current_music_key = None

def init_mixer():
    if not pygame.mixer.get_init():
        try: pygame.mixer.init();
        except pygame.error as e: print(f"Erreur init mixer: {e}")

def play_music(key, loops=-1, volume=0.5, fade_ms=1000):
    global current_music_key
    init_mixer()
    if not pygame.mixer.get_init(): return
    if key not in music_paths: print(f"Err: Clé musique '{key}' NI."); return
    music_file = music_paths[key]
    if not os.path.exists(music_file): print(f"Err: Fichier musical NI : {music_file}"); return

    try:
        if current_music_key == key and pygame.mixer.music.get_busy(): return
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)
            pygame.time.wait(fade_ms)
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops)
        current_music_key = key
    except pygame.error as e:
        print(f"Err lecture/chargement musique {music_file}: {e}"); current_music_key = None

def stop_music():
    global current_music_key; init_mixer()
    if not pygame.mixer.get_init(): return
    pygame.mixer.music.stop(); pygame.mixer.music.unload(); current_music_key = None

def fadeout_music(time_ms):
    init_mixer()
    if not pygame.mixer.get_init(): return
    pygame.mixer.music.fadeout(time_ms)

def set_volume(volume):
    init_mixer()
    if not pygame.mixer.get_init(): return
    if 0.0 <= volume <= 1.0: pygame.mixer.music.set_volume(volume)
    else: print("Volume invalide.")

def is_playing(key=None):
    init_mixer()
    if not pygame.mixer.get_init(): return False
    if key: return pygame.mixer.music.get_busy() and current_music_key == key
    return pygame.mixer.music.get_busy()