import pygame

pygame.init()
running = True
while running:
    screen = pygame.display.set_mode((1200, 750))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False