import pygame

pygame.init()

screen_width = 1200
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Dunk & Degree")

background = pygame.image.load("image/background.png")
basket = pygame.image.load("image/basket.png")
basket = pygame.transform.scale(basket, (400, 350))

running = True

def check_event ():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def show_img():
    screen.blit(background, (0, 0))
    screen.blit(basket, (850, 50))

while running :
    check_event()
    show_img()
    pygame.display.flip()

pygame.quit()