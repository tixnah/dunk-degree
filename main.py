from check_events import *
from level import *

running = True

difficulty_selector = 0

level = 0
score = 0

while running :     # main game loop

    running, game_launched = menu_event()   # Check for the user input and events
    show_img()      # Draw image on the screen
    show_overlay()  # Draw the case of the avatars and balls

    if game_launched:
        difficulty_selector, level = basket_hoop(difficulty_selector, level, score)  # Move basket

    pygame.display.flip()   # Update the display

pygame.quit()   # Quit pygame properly