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
basket_img = pygame.transform.smoothscale(basket_img, (200, 175))

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
basket_x = 900
basket_y = 175
basket_direction = -1
state = "horizontal_left"

def basket_hoop (difficulty_selector, level, score):
    global screen, basket_x, basket_y, basket_direction,state

    diff = difficulty[difficulty_selector]


    if diff == "Easy" or diff == "Normal":
        max_level = 3
    else :
        max_level = 5






    if diff == "Normal" and level < max_level:
        basket_speed = 0.5

        if level == 0:
            if basket_x >= 900:
                basket_direction = -1

            elif basket_x <= 700:
                basket_direction = 1
            basket_x += basket_direction * basket_speed


        if level == 1:
            if basket_y >= 350:
                basket_direction = -1

            elif basket_y <= 175:
                basket_direction = 1
            basket_y += basket_direction * basket_speed

        if level == 2:
            if state == "horizontal_left":
                basket_x += basket_direction * basket_speed
                if basket_x <= 700:
                    basket_x = 700
                    state = "horizontal_right"
                    basket_direction = 1  # vers le bas

            elif state == "vertical_down":
                basket_y += basket_direction * basket_speed
                if basket_y >= 400:
                    basket_y = 400
                    state = "vertical_up"
                    basket_direction = -1  # vers le haut

            elif state == "vertical_up":
                basket_y += basket_direction * basket_speed
                if basket_y <= 175:
                    basket_y = 175
                    state = "horizontal_left"
                    basket_direction = -1  # vers la gauche

            elif state == "horizontal_right":
                basket_x += basket_direction * basket_speed
                if basket_x >= 900:
                    basket_x = 900
                    state = "vertical_down"
                    basket_direction = 1  # vers le bas







    if diff == "Intermediate" and level < max_level :
        basket_speed = 1


        if level == 0:
            if basket_x >= 900:
                basket_direction = -1

            elif basket_x <= 600:
                basket_direction = 1
            basket_x += basket_direction * basket_speed


        if level == 1:
            if basket_y >= 350:
                basket_direction = -1

            elif basket_y <= 100:
                basket_direction = 1
            basket_y += basket_direction * basket_speed


        if level == 2:
            if state == "horizontal_left":
                basket_x += basket_direction * basket_speed
                if basket_x <= 600:
                    basket_x = 600
                    state = "horizontal_right"
                    basket_direction = 1  # vers le bas

            elif state == "vertical_down":
                basket_y += basket_direction * basket_speed
                if basket_y >= 400:
                    basket_y = 400
                    state = "vertical_up"
                    basket_direction = -1  # vers le haut

            elif state == "vertical_up":
                basket_y += basket_direction * basket_speed
                if basket_y <= 175:
                    basket_y = 175
                    state = "horizontal_left"
                    basket_direction = -1  # vers la gauche

            elif state == "horizontal_right":
                basket_x += basket_direction * basket_speed
                if basket_x >= 900:
                    basket_x = 900
                    state = "vertical_down"
                    basket_direction = 1  # vers le bas



        if level == 3 :
            if basket_y >= 350:
                basket_direction = -1

            elif basket_y <= 80:
                basket_direction = 1

            basket_y += basket_direction * basket_speed
            basket_x += 0.5 * basket_direction * basket_speed


        if level == 4:

            if basket_y >= 350:
                basket_direction = 1

            elif basket_y <= 80:
                basket_direction = -1

            basket_y -= basket_direction * basket_speed
            basket_x += 0.5 * basket_direction * basket_speed



    if diff == "Difficult" and level < max_level :
        basket_speed = 2


        if level == 0 : #T
            if state == "horizontal_left":
                basket_x += basket_direction * basket_speed
                if basket_x <= 700:
                    basket_x = 700
                    state = "horizontal_right"
                    basket_direction = 1  # vers la droite

            elif state == "vertical_down":
                basket_y += basket_direction * basket_speed
                if basket_y >= 175:
                    basket_y = 175
                    state = "vertical_up"
                    basket_direction = -1  # vers le haut

            elif state == "vertical_up":
                basket_y += basket_direction * basket_speed
                if basket_y <= 175:
                    basket_y = 175
                    state = "horizontal_left"
                    basket_direction = -1  # vers la gauche

            elif state == "horizontal_right":
                basket_x += basket_direction * basket_speed
                if basket_x >= 900:
                    basket_x = 900
                    state = "vertical_down"
                    basket_direction = 1  # vers le bas



        if level == 1 : #diagonale
            if basket_y >= 350:
                basket_direction = -1

            elif basket_y <= 80:
                basket_direction = 1

            basket_y += basket_direction * basket_speed
            basket_x += 0.5 * basket_direction * basket_speed



        if level == 2 : #triangle
            if state == "horizontal_left":
               state = "vertical_down"

            if state == "vertical_down":
                basket_y -= basket_direction * basket_speed
                basket_x += 0.5 * basket_direction * basket_speed
                if basket_y >= 400:
                    basket_y = 400
                    state = "horizontal_right"
                    basket_direction = -1

            if state == "horizontal_right":
                basket_x -= basket_direction * basket_speed
                if basket_x >= 900:
                    basket_x = 900
                    state = "vertical_up"
                    basket_direction = 1

            if state == "vertical_up":
                basket_y -= basket_direction * basket_speed
                basket_x -= 0.5 * basket_direction * basket_speed
                if basket_y <= 175:
                    basket_y = 175
                    state = "vertical_down"
                    basket_direction = -1  # vers la gauche



        if level == 3: #carré
            if state == "horizontal_left":
                basket_x += basket_direction * basket_speed
                if basket_x <= 700:
                    basket_x = 700
                    state = "vertical_down"
                    basket_direction = 1

            elif state == "vertical_down":
                basket_y += basket_direction * basket_speed
                if basket_y >= 400:
                    basket_y = 400
                    state = "horizontal_right"
                    basket_direction = 1

            elif state == "horizontal_right":
                basket_x += basket_direction * basket_speed
                if basket_x >= 900:
                    basket_x = 900
                    state = "vertical_up"
                    basket_direction = -1

            elif state == "vertical_up":
                basket_y += basket_direction * basket_speed
                if basket_y <= 175:
                    basket_y = 175
                    state = "horizontal_left"
                    basket_direction = -1




        if level == 4 : #hexagone
            if state == "horizontal_left":
                basket_x += basket_direction * basket_speed
                if basket_x <= 800:
                    basket_x = 800
                    state = "vertical_down1"
                    basket_direction = 1

            elif state == "vertical_down1":
                basket_y += basket_direction * basket_speed
                basket_x -= 0.5 * basket_direction * basket_speed
                if basket_y >= 265:
                    basket_y = 265
                    state = "vertical_down2"
                    basket_direction = 1

            elif state == "vertical_down2":
                basket_y += basket_direction * basket_speed
                basket_x += 0.5 * basket_direction * basket_speed
                if basket_y >= 400 :
                    basket_y = 400
                    state = "horizontal_right"
                    basket_direction = 1

            elif state == "horizontal_right":
                basket_x += basket_direction * basket_speed
                if basket_x >= 900:
                    basket_x = 900
                    state = "vertical_up1"
                    basket_direction = -1

            elif state == "vertical_up1":
                basket_y += basket_direction * basket_speed
                basket_x -= 0.5 * basket_direction * basket_speed
                if basket_y <= 265:
                    basket_y = 265
                    state = "vertical_up2"
                    basket_direction = -1

            elif state == "vertical_up2":
                basket_y += basket_direction * basket_speed
                basket_x += 0.5 * basket_direction * basket_speed
                if basket_y <= 130:
                    basket_y = 130
                    state = "horizontal_left"
                    basket_direction = -1













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
