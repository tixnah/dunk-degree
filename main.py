import pygame
from check_events import menu_event,show_img

running = True

while running :     # \ main game loop
    menu_event()   # \ Check for the user input and events
    show_img()      # \ Draw image on the screen
    pygame.display.flip()   # \ Update the display

pygame.quit()   # \ Quit pygame properly