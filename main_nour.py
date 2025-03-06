import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 750))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color
    screen.fill("light blue")
    pygame.display.flip()
    #fps
    clock.tick(60)
pygame.quit()