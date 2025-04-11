from test_audrey import menu_event
from test_audrey import show_img
import time
import pygame

running = True

while running :     # \ main game loop
    menu_event()   # \ Check for the user input and events
    show_img()      # \ Draw image on the screen
    pygame.display.flip()   # \ Update the display


pygame.quit()   # \ Quit pygame properly



