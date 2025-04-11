import pygame
import random
import time
import main_nour



#  Initialisation of Pygame
pygame.init()


#Nour's program

#Screen
screen_width = 1200
screen_height = 675
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Dunk & Degree")

background = pygame.image.load("background.png")
basket_img = pygame.image.load("basket.png")
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



