import pygame

#  Initialisation of Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 1200
# Width
screen_height = 675
# Height
screen = pygame.display.set_mode((screen_width, screen_height))
# Create the game window

basket_img = pygame.image.load("image/basket.png").convert_alpha()
basket_img = pygame.transform.smoothscale(basket_img, (400, 350))

#Level's parameter

difficulty_level = {
    "Easy": [1, 2, 3],
    # basket doesn't move
    "Normal": [1, 2, 3],
    # left to right, up to done, every direction // basket move slowly
    "Intermediate": [1 ,2 ,3, 4, 5],
    # left to right / up to down / left, right, up and down / diagonals // basket move an average speed
    "Difficult" : [1, 2, 3, 4, 5],
    # left to right / up to down / left, right, up and down / diagonals
}

difficulty = ["Easy", "Normal", "Intermediate", "Difficult"]
diff = difficulty[0]
level = 0

def basket_hoop (diff, level):
    global difficulty_level
    global screen

    if diff == "Easy" or diff == "Normal":
        max_level = 3

    else :
        max_level = 5

    if diff == "Easy" and level < max_level:
        basket_x = 900
        basket_y = 100
        basket_speed = 0

    if diff == "Normal" and level < max_level:
        basket_x = 900
        basket_y = 100
        basket_speed = 1

    if diff == "Intermediate" and level < max_level :
        basket_x = 900
        basket_y = 100
        basket_speed = 2

    if diff == "Difficult" and level < max_level :
        basket_x = 900
        basket_y = 100
        basket_speed = 3

    screen.blit(basket_img, (basket_x, basket_y))

    return