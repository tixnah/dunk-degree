import pygame
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

menu = pygame.image.load("image/menu.png")
# Load the image "menu.png" as the background named "menu"
guide = pygame.image.load("image/guide.png")
# Load the image "guide.png" as the background named "guide"
game = pygame.image.load("image/background.png")
# Load the image "background.png" as the background named "game"
parameter_on = pygame.image.load("image/parameter_on.png")
# Load the image "parameter_on.png" as the background named "parameter_on"
parameter_off = pygame.image.load("image/parameter_off.png")
# Load the image "parameter_off.png" as the background named "parameter_off"

##############################################################
#REMEMBER TO ADD IN THE DEF SHOW_ING - AT THE END OF THE CODE
##############################################################


# LOAD ALL THE IMAGES OBJECTS

ball_violet = pygame.image.load("image/ball_violet.png")
# Load the image "ball_violet.png" as the background named "ball_violet"
sheep_1 = pygame.image.load("image/mouton-face.png")
# Load the image "mouton-face.png" as the background named "sheep_1"
click = pygame.image.load("image/click.png")
click = pygame.transform.scale(click, (400, 350))
# Load the image "click.png" as "click"


# DEFINE THE BUTTONS

# IN THE MENU BUTTONS
start_button_rect = pygame.Rect(132,556,106,35)
# Button Start in the Menu
guide_button_rect = pygame.Rect(382,556,119,35)
# Button to go to the Guide page from the Menu
parameter_button_rect = pygame.Rect(686,556,119,35)
# Button to go to the Parameter page from the Menu
quit_menu_button_rect = pygame.Rect(963,556,79,35)
# Button to quit the window when you are in the Menu

# IN PARAMETER & GUIDE BUTTON
return_menu_button_rect = pygame.Rect(830,529,237,66)
# Button to go back to the Menu work both for the background "guide" and "parameter"

# IN PARAMETER BUTTONS

#MUSIC BUTTONS
music_on_button_rect = pygame.Rect(829,189,76,41)
# Button to have the music ON when it was OFF
music_off_button_rect = pygame.Rect(1002,189,76,41)
# Button to have the music OFF when it was ON

#BALL BUTTONS
violet_ball_button_rect = pygame.Rect(651,370,115,102)
# Select Purple Ball
blue_ball_button_rect = pygame.Rect(824,370,115,102)
# Select Blue Ball
orange_ball_button_rect = pygame.Rect(996,370,115,102)
# Select Orange Ball

#AVATAR BUTTONS
avatar_1_button_rect = pygame.Rect(89,243,115,178)
# 1st avatar - at the left - Girl n 1
avatar_2_button_rect = pygame.Rect(266,243,115,178)
# 2nd avatar - at the middle - Girl n 2
avatar_3_button_rect = pygame.Rect(449,243,115,178)
# 3rd avatar - at the right - Boy


# IN GAME BUTTONS
quit_game_button_rect = pygame.Rect(1001,20,772,42)

# GAME LOOP CONTROL
running = True      # Game loop
current_screen = "menu"
pygame.display.set_caption("Dunk & Degree - Menu")




def menu_event ():
    global running, current_screen  # \ Access the global 'running" variable
    music = True
    avatar = 1
    ball = 1
    pos = None

    for event in pygame.event.get():    # \ Iterate through all pygame event
        if event.type == pygame.QUIT:   # \ If the user clicks the close button ...
            running = False     # \ ... Set running become False and you exit the loop
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos     # \ Collect the position of the click

    if pos is not None:

        #GESTION IN THE MENU
        # if we are in the menu page
        if current_screen == "menu":

            # if the click is on the button play
            if start_button_rect.collidepoint(pos):
                current_screen = "game"
                pygame.display.set_caption("Dunk & Degree - Game")
                pygame.display.flip()
                print("Start button pressed - Starting...\nThe Game Begins!\n")

            # if the click is on the button guide
            elif guide_button_rect.collidepoint(pos):
                current_screen = "guide"    # display the guide image
                pygame.display.set_caption("Dunk & Degree - Guide")     # "Dunk & Degree - Guide" become the title of the window
                pygame.display.flip()       # Refresh the image
                time.sleep(0.4)
                print("\nGuide button pressed - Switch to the guide page...")
                time.sleep(0.5)
                print("You are in the Guide.")
                time.sleep(0.5)
                print("\nLearn How To Play Here! \nAnd once done go back to the Menu.\n")

            # if the click is on the button parameter
            elif parameter_button_rect.collidepoint(pos):
                if music == True :
                    current_screen = "parameter_on"    # display the parameter image
                elif music == False :
                    current_screen = "parameter_off"
                pygame.display.set_caption("Dunk & Degree - Parameter")     # "Dunk & Degree - Parameter" become the title of the window
                pygame.display.flip()       # Refresh the image
                time.sleep(0.4)
                print("\nParameter button pressed - Switch to the parameter page...")
                time.sleep(0.5)
                print("\nYou are in the Parameter. \nChoose your option or go back to the Menu.\n")

            # if the click is on the button quit
            elif quit_menu_button_rect.collidepoint(pos):
                print("Quit button pressed - Quitting the game...")
                running = False  # Quit the game

        #GESTION IN THE GUIDE
        # if we are in the guide
        if current_screen == "guide":
            # if the click is on the button return menu
            if return_menu_button_rect.collidepoint(pos):
                current_screen = "menu"
                pygame.display.flip()  # Refresh the image
                pygame.display.set_caption("Dunk & Degree - Menu")    # display the menu image
                time.sleep(0.4)
                print("Return to the Menu button pressed - Switch to the return menu page...\nYou are in the Menu.")
                time.sleep(0.2)
                print("\nDo You Want Start Playing ? \nIf 'Yes' Click on the START button!\n")
                print("If you want to learn how to play Click on the Guide Button. \nIf you want to change your Avatar, the Basket Ball or even Mute the Music Click on the Option Button.")

        #GESTION OF THE PARAMETER
        #if we are in the parameter
        if current_screen in ["parameter_on", "parameter_off"]:
            if return_menu_button_rect.collidepoint(pos):
                current_screen = "menu"
                pygame.display.flip()  # Refresh the image
                pygame.display.set_caption("Dunk & Degree - Menu")  # display the menu image
                time.sleep(0.4)
                print("Return to the Menu button pressed - Switch to the return menu page...\nYou are in the Menu.")
                time.sleep(0.2)
                print("\nDo You Want Start Playing ? \nIf 'Yes' Click on the START button!\n")
                print("If you want to learn how to play Click on the Guide Button. \nIf you want to change your Avatar, the Basket Ball or even Mute the Music Click on the Option Button.")
            #MUSIC
            if (current_screen == "parameter_on") & (music_off_button_rect.collidepoint(pos)):
                music = False
                print("The Music is OFF.")
                current_screen = "parameter_off"
                pygame.display.flip()  # Refresh the image
            elif (current_screen == "parameter_off") & (music_on_button_rect.collidepoint(pos)):
                music = True
                print("The Music is ON.")
                current_screen = "parameter_on"
                pygame.display.flip()  # Refresh the image

            #GESTION OF THE AVATAR
            if avatar_1_button_rect.collidepoint(pos):
                avatar = 1
                print("the first avatar has been chosen")
            elif avatar_2_button_rect.collidepoint(pos):
                avatar = 2
                print("the second avatar has been chosen")
            elif avatar_3_button_rect.collidepoint(pos):
                avatar = 3
                print("the third avatar has been chosen")

            #GESTION OF THE BALL
            if violet_ball_button_rect.collidepoint(pos):
                ball = 1
                print("the purple ball has been chosen")
            elif blue_ball_button_rect.collidepoint(pos):
                ball = 2
                print("the blue ball has been chosen")
            elif orange_ball_button_rect.collidepoint(pos):
                ball = 3
                print("the orange ball has been chosen")

        #GESTION IN THE GAME
        if current_screen == "game":
            if quit_game_button_rect.collidepoint(pos):
                current_screen = "menu"
                pygame.display.flip()  # Refresh the image
                pygame.display.set_caption("Dunk & Degree - Menu")    # display the menu image
                time.sleep(0.4)
                print("Return to the Menu button pressed - Switch to the return menu page...\nYou are in the Menu.")
                time.sleep(0.2)
                print("\nDo You Want Start Playing ? \nIf 'Yes' Click on the START button!\n")
                print("If you want to learn how to play Click on the Guide Button. \nIf you want to change your Avatar, the Basket Ball or even Mute the Music Click on the Option Button.")
    return running

def show_img():     # Function to display the images on the screen
    if current_screen == "menu":
        screen.blit(menu, (0, 0))     # Draw the background "menu" at position (0,0)

    if current_screen == "guide":
        screen.blit(guide, (0, 0))     # Draw the background "guide" at position (0,0)

    if current_screen == "game":
        screen.blit(game, (0, 0))     # Draw the background "game" at position (0,0)

    if current_screen == "parameter_on":
        screen.blit(parameter_on, (0, 0))     # Draw the background "parameter_on" at position (0,0)

    if current_screen == "parameter_off":
        screen.blit(parameter_off, (0, 0))     # Draw the background "parameter_off" at position (0,0)

while running :     # \ main game loop
    menu_event()   # \ Check for the user input and events
    show_img()      # \ Draw image on the screen
    pygame.display.flip()   # \ Update the display

pygame.quit()   # \ Quit pygame properly