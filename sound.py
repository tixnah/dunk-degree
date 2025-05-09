import pygame
import time

#Initialization of pygame.mixer
pygame.mixer.init()

#Music File
menu_music = "music_menu.mp3"
score_music = "music_score_de_fin.mp3"

# Music for each level
level_music = {
    1: "music_palier_1.mp3",
    2: "music_palier_2.mp3",
    3: "music_palier_3.mp3",
    4: "music_palier_4.mp3",
}
fade_in_duration = 500 #0,5 second in milliseconds

def play_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer_music.play(0,0, 5000)

def play_menu_music():
    play_music(menu_music)

def play_level_music(level):
    if level in level_music:
        play_music(level_music[level])
    else:
        pygame.mixer_music.stop()

def play_end_music():
    pygame.mixer_music.load(score_music)
    pygame.mixer_music.play(0,0,5000)



# --- Simple Game Simulation --- EN GROS LE MAIN
try:
    # 1. Main menu
    play_menu_music()
    time.sleep(5)  # Simulate player staying in the menu for 5 seconds

    # 2. Level progression
    current_level = 0
    for next_level in [1, 2, 3,4]:
        if next_level != current_level:
            current_level = next_level
            play_level_music(current_level)
        time.sleep(5)  # Simulate player staying at each level for 5 seconds

    # 3. Display final score
    play_end_music()
    time.sleep(5)

except KeyboardInterrupt:
    pygame.mixer.music.stop() # pause