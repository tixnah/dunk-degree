import pygame
# Import the pygame module

import time


pygame.init()
# Initialize all pygame modules

# Set up the screen dimensions
screen_width = 1200
# Width
screen_height = 675
# Height
screen = pygame.display.set_mode((screen_width, screen_height))
# Create the game window



pygame.display.set_caption("Dunk & Degree")
# Give the name "Dunk & Degree" as the title of the window


# LOAD ALL THE IMAGES BACKGROUND

menu = pygame.image.load("menu.png")
# Load the image "menu.png" as the background named "menu"
guide = pygame.image.load("guide.png")
# Load the image "guide.png" as the background named "guide"
parameter = pygame.image.load("parameter.png")
# Load the image "parameter.png" as the background named "parameter"
background = pygame.image.load("background.png")
# Load the image "background.png" as the background named "background_game_1"


# LOAD ALL THE IMAGES OBJECTS

ball_violet = pygame.image.load("ball_violet.png")
# Load the image "ball_violet.png" as the background named "ball_violet"
sheep_1 = pygame.image.load("mouton-face.png")
# Load the image "mouton-face.png" as the background named "sheep_1"


# DEFINE THE BUTTONS

start_button_rect = pygame.Rect(132,556,106,35)
# Button Start in the Menu
guide_button_rect = pygame.Rect(382,556,119,35)
# Button to go to the Guide page from the Menu
parameter_button_rect = pygame.Rect(686,556,119,35)
# Button to go to the Parameter page from the Menu

quit_menu_button_rect = pygame.Rect(963,556,79,35)
# Button to quit the game when you are in the Menu
return_menu_button_rect = pygame.Rect(830,529,237,66)
# Button to go back to the Menu
# Return_menu_button_rect work both for the background "guide" and "parameter"


# GAME LOOP CONTROL
running = True      # \ Game loop
current_screen = "menu"
pygame.display.set_caption("Dunk & Degree - Menu")


def check_event ():
    global running, current_screen  # \ Access the global 'running" variable
    pos = None

    for event in pygame.event.get():    # \ Iterate through all pygame event
        if event.type == pygame.QUIT:   # \ If the user clicks the close button ...
            running = False     # \ ... Set running become False and you exit the loop

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos     # \ Collect the position of the click

    if pos is not None:

        # \ if we are in the menu page
        if current_screen == "menu":

            # \ if the click is on the button play
            if start_button_rect.collidepoint(pos):
                current_screen = "background"
                pygame.display.set_caption("Dunk & Degree - Game")
                pygame.display.flip()
                print("Start button pressed - Starting...\nThe Game Begins!\n")

                pass # CODE FOR THE GAME

            # \ if the click is on the button guide
            elif guide_button_rect.collidepoint(pos):
                current_screen = "guide"    # \ display the guide image
                pygame.display.set_caption("Dunk & Degree - Guide")     # \ "Dunk & Degree - Guide" become the title of the window
                pygame.display.flip()       # \ Refresh the image
                time.sleep(0.4)
                print("\nGuide button pressed - Switch to the guide page...")
                time.sleep(0.5)
                print("You are in the Guide.")
                time.sleep(0.5)
                print("\nLearn How To Play Here! \nAnd once done go back to the Menu.\n")


            # \ if the click is on the button parameter
            elif parameter_button_rect.collidepoint(pos):
                current_screen = "parameter"    # \ display the parameter image
                pygame.display.set_caption("Dunk & Degree - Parameter")     # \ "Dunk & Degree - Parameter" become the title of the window
                pygame.display.flip()       # \ Refresh the image
                time.sleep(0.4)
                print("\nParameter button pressed - Switch to the parameter page...")
                time.sleep(0.5)
                print("\nYou are in the Parameter. \nChoose your option or go back to the Menu.\n")


            # \ if the click is on the button quit
            elif quit_menu_button_rect.collidepoint(pos):
                print("Quit button pressed - Quitting the game...")
                running = False       # \ Quit the game


        # \ if we are in the guide or in the parameter page
        if current_screen in ["guide", "parameter"]:

            # \ if the click is on the button return menu
            if return_menu_button_rect.collidepoint(pos):
                current_screen = "menu"
                pygame.display.flip()  # \ Refresh the image
                pygame.display.set_caption("Dunk & Degree - Menu")    # \ display the menu image
                time.sleep(0.4)
                print("Return to the Menu button pressed - Switch to the return menu page...\nYou are in the Menu.")
                time.sleep(0.2)
                print("\nDo You Want Start Playing ? \nIf 'Yes' Click on the START button!\n")
                print("If you want to learn how to play Click on the Guide Button. \nIf you want to change your Avatar, the Basket Ball or even Mute the Music Click on the Option Button.")



def show_img():     # \ Function to display the images on the screen
    if current_screen == "menu":
        screen.blit(menu, (0, 0))     # \ Draw the background "menu" at position (0,0)
    if current_screen == "guide":
        screen.blit(guide, (0, 0))     # \ Draw the background "guide" at position (0,0)
    if current_screen == "parameter":
        screen.blit(parameter, (0, 0))     # \ Draw the background "parameter" at position (0,0)


while running :     # \ main game loop
    check_event()   # \ Check for the user input and events
    show_img()      # \ Draw image on the screen
    pygame.display.flip()   # \ Update the display


pygame.quit()   # \ Quit pygame properly