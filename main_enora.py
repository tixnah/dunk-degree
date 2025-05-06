import pygame
import time

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

"""
difficulty_level = {
    "Easy": [1, 2, 3],
    # basket doesn't move
    "Normal": [1, 2, 3],
    # left to right, up to down, every direction // basket move slowly
    "Intermediate": [1 ,2 ,3, 4, 5],
    # left to right / up to down / left, right, up and down / diagonals // basket move an average speed
    "Difficult" : [1, 2, 3, 4, 5],
    # left to right / up to down / left, right, up and down / diagonals
}
"""
difficulty = ["Easy", "Normal", "Intermediate", "Difficult"]
basket_x = 800
basket_y = 100
basket_direction = -1

def basket_hoop (difficulty_selector, level, score):
    global screen, basket_x, basket_y, basket_direction

    diff = difficulty[difficulty_selector]


    if diff == "Easy" or diff == "Normal":
        max_level = 3
    else :
        max_level = 5

    if diff == "Normal" and level < max_level:
        basket_speed = 0.5
        tmp = False
        if level == 0:
            if basket_x >= 800:
                basket_direction = -1

            elif basket_x <= 600:
                basket_direction = 1
            basket_x += basket_direction * basket_speed




        if level == 1:
            basket_speed = 1
            tmp = False

            basket_y += basket_direction * basket_speed

            if basket_y >= 500:
                basket_y = 500
                basket_direction = -1
            elif basket_y <= 100:
                basket_y = 100


        if level == 2:
            tmp = False
            if not tmp:
                if basket_x > 600 :
                    basket_x -= basket_speed
                if basket_x<=600:
                    basket_x += basket_speed
                if basket_x == 800 :
                    tmp = True

            elif tmp:
                if basket_y > 200:
                    basket_y -= basket_speed
                if basket_y <= 200:
                    basket_y += basket_speed
                if basket_y == 100:
                    tmp = False







    if diff == "Intermediate" and level < max_level :
        basket_x = 800
        basket_y = 100
        basket_speed = 2


    if diff == "Difficult" and level < max_level :
        basket_x = 800
        basket_y = 100
        basket_speed = 3

    if score % 100 and score != 0 :
        if level < max_level - 1:
            level += 1
            basket_x = 800
            basket_y = 100
        else:
            difficulty_selector += 1
            level = 0


    screen.blit(basket_img, (basket_x, basket_y))

    return difficulty_selector, level
