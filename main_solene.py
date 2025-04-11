import pygame

pygame.init()

# Game settings
DURATION = 45  # duration in seconds
screen = pygame.display.set_mode((1200, 750))
font = pygame.font.Font(None, 50)

# Start Time
start_time = pygame.time.get_ticks()

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


def check_event():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


def show_img():
    screen.blit(background, (0, 0))
    screen.blit(basket, (850, 50))


while running:
    check_event()
    show_img()
    pygame.display.flip()

    #timer
    elapsed_time = (pygame.time.get_ticks() - start_time) // 2500

    # Check if the time is up
    if elapsed_time >= DURATION:
        print("⏳ Time's up! Game over !")
        running = False

    # Show remaining time
    time_text = font.render(f"Remaining Time : {DURATION - elapsed_time}s", True, (255, 255, 255))
    screen.blit(time_text, (40, 30))

    pygame.display.flip()

pygame.quit()

"""
running = True
while running:
    screen.fill((0,0,0))  # Black Background
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    # Check if the time is up
    if elapsed_time >= DURATION:
        print("⏳ Time's up! Game over !")
        running = False

    # Show remaining time
    time_text = font.render(f"Remaining Time : {DURATION - elapsed_time}s", True, (255, 255, 255))
    screen.blit(time_text, (50, 50))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

# code for transparency and opacity of an image

fond_color = (255,255,255)
FPS = 30
pygame.init()

clock = pygame.time.Clock()

fond_background = pygame.image.load("background.png")

width, height = fond_background.get_size()

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dunk & Degree")
window.fill(fond_color)

fond_background = fond_background.convert()
fond_background.set_alpha(127)

background = pygame.image.load("background.png")
background_alpha = background.copy()

background = background.convert()
background_alpha = background_alpha.convert_alpha()
"""