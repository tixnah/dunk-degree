import pygame
import random
import time
import main_nour
import main_audrey



#  Initialisation of Pygame
pygame.init()


#Nour's program

#Screen
screen_width = 1200
screen_height = 675
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Dunk & Degree")

background = pygame.image.load("image/background.png")
basket_img = pygame.image.load("image/basket.png")
basket_img = pygame.transform.scale(basket_img, (400, 350))

running = True

def check_event ():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def show_img():
    screen.blit(background, (0, 0))
    screen.blit(basket_img, (850, 50))

while running :
    check_event()
    show_img()
    pygame.display.flip()

#End Nour's program



# ball's library

ball_orange_img = pygame.image.load ("image/ball_orange.png")
ball_violet_img = pygame.image.load ("image/ball_violet.png")
ball_blue_img = pygame.image.load ("image/ball_blue.png")


# image chose






# basket's parameter

basket_x = screen_width // 2
basket_y = screen_height
basket_speed = 0



#Level's parameter

difficulty_level = {
    "Easy": {"level" : [1, 2, 3]},
    # basket doesn't move
    "Normal": {"level" : [1, 2, 3]},
    # left to right, up to done, every direction // basket move slowly
    "Intermediate": {"level": [1 ,2 ,3, 4, 5]},
    # left to right / up to down / left, right, up and down / diagonals // basket move an average speed
    "Difficult" : {"level" : [1, 2, 3, 4, 5]},
    # left to right / up to down / left, right, up and down / diagonals
}




# Move basket



def move_basket ():
    global basket_x, basket_y, basket_speed
    score = 0





    # Easy : the basket doesn't move / 3 games
    if difficulty_level == "Easy" :
        basket_speed = 0
        i = 0
        while score :
            mode = difficulty_level["Easy"]["level"][i]
            i += 1






    #Normal : left to right, up to done, every direction // basket move slowly
    if difficulty_level == "Normal" :
        basket_speed = 1.0
        i = 0
        while score :
            mode = difficulty_level["Normal"]["level"][i]

            # left to right
            if i == 0 :
                basket_x -= 16
                basket_x += 16
                while score:
                    i += 1

            # up to down
            if i == 1 :
                basket_x = screen_width // 2
                basket_y += 16
                basket_y -= 16
                while score:
                    i += 1

            # every direction
            if i == 2 :
                basket_x = screen_width // 2
                basket_x -= 16
                basket_x += 16
                basket_y -= 16
                basket_y += 16
                while score:
                    i += 1






    # Intermediate : left to right / up to down / left, right, up and down / diagonals // basket move an average speed
    if difficulty_level == "Intermediate" :
        basket_speed = 3.0
        i = 0
        while score :
            mode = difficulty_level["Intermediate"]["level"][i]
            if i == 0:
                # left to right
                basket_x -= 16
                basket_x += 16
                while score:
                    i += 1

            if i == 1:
                # up to down
                basket_x = screen_width // 2
                basket_y += 16
                basket_y -= 16
                while score:
                    i += 1

            if i == 2:
                # left, right, up and down
                basket_x = screen_width // 2
                basket_x -= 16
                basket_x += 16
                basket_y -= 16
                basket_y += 16
                while score:
                    i += 1

            if i == 3:
                # diagonals
                while x!= 0:
                    basket_x +=1
                    basket_y +=1
                while x == 0:
                    basket_x -= 1
                    basket_y -= 1

                while score :
            i += 1





    # Difficulty :
    if difficulty_level == "Difficulty" :
        basket_speed = 6.0
        i = 0
        while score :
            mode = difficulty_level["Difficult"]["level"][i]
            i += 1



