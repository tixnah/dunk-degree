import pygame
import math

# Paramètres généraux
g = 300  # gravité (pixels/s²)
ball_radius = 15
ball_color = (255, 0, 0)

# Variables globales pour la balle
ball_x = 100
ball_y = 500
v_x = 300  # vitesse horizontale en px/s
v_y = -300  # vitesse verticale initiale en px/s
ball_active = False  # est-ce que la balle est en vol ?
start_time = 0

def start_ball():
    global ball_x, ball_y, v_x, v_y, ball_active, start_time
    ball_x = 100
    ball_y = 500
    v_x = 300
    v_y = -300  # vers le haut
    start_time = pygame.time.get_ticks() / 1000  # temps en secondes
    ball_active = True

def update_ball():
    global ball_x, ball_y, v_y
    dt = 0.016  # on suppose 60 fps ≈ 16 ms
    ball_x += v_x * dt
    ball_y += v_y * dt + 0.5 * g * dt**2
    v_y += g * dt

def draw_ball(screen):
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)

def handle_ball():
    global ball_active, ball_x, ball_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.K_SPACE :
            if not ball_active:
                start_ball()

    if ball_active:
        update_ball()
        draw_ball(pygame.display.get_surface())

        if ball_y > 720 or ball_x > 1280:
            ball_active = False