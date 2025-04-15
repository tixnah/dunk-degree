from test_audrey import menu_event
from test_audrey import show_img
from main_enora import*
import time
import pygame

running = True
game_launch = False
while running : # \ main game loop
    show_img() #\ Draw image on the screen
    if not game_launch :
        game_launch = menu_event()   # \ Check for the user input and events

    if game_launch :
        basket_hoop(diff,level)

    pygame.display.flip()   # \ Update the display


pygame.quit()   # \ Quit pygame properly



