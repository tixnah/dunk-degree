import pygame

pygame.init()

# Game settings
DURATION = 60  # duration in seconds
screen = pygame.display.set_mode((1200, 750))
pygame.display.set_caption("Dunk & Degree")

font = pygame.font.Font(None, 40)

# Load images
background = pygame.image.load("image/background.png")
basket = pygame.image.load("image/basket.png")
basket = pygame.transform.scale(basket, (400, 350))

# Start Time
start_time = pygame.time.get_ticks()
running = True

def check_event():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

while running:
    check_event()

    # Draw background first
    screen.blit(background, (0, 0))

    # Draw basket
    screen.blit(basket, (850, 50))

    # Timer
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    if elapsed_time >= DURATION:
        print("⏳ Time's up! Game over !")
        running = False

    # Draw timer text
    time_text = font.render(f"Time : {DURATION - elapsed_time}s", True, (255, 255, 255))
    screen.blit(time_text, (40, 30))

    # Update screen once
    pygame.display.flip()

pygame.quit()

# Score counter

import pygame

pygame.init()

basket = pygame.transform.scale(basket, (400, 350))

# Fonts
font = pygame.font.Font(None, 50)

# Ball position
# ball_pos = ICI FAUT METTRE LIMAGE DE LA BALLE
ball_pos.top = int(600, 500) # Starting position

# Basket zone (hitbox) for scoring
basket_zone = pygame.Rect(900, 200, 100, 30)  # Adjust this to fit your hoop

# Score
score = 0
scored = False

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(basket, (850, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Ball movement (for test, arrow keys) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_pos.x -= 5
    if keys[pygame.K_RIGHT]:
        ball_pos.x += 5
    if keys[pygame.K_UP]:
        ball_pos.y -= 5
    if keys[pygame.K_DOWN]:
        ball_rect.y += 5

    # --- Check collision with basket zone ---
    if ball_pos.colliderect(basket_zone):
        if not scored:
            score += 1
            scored = True
    else:
        scored = False  # Reset when ball leaves the zone

    # Draw ball
    screen.blit(ball_img, ball_rect)

    # Draw score
    score_text = font.render(f"Score : {score}", True, (255, 255, 255))
    screen.blit(score_text, (40, 80))

    # Optional: visualize the basket zone for debugging
    # pygame.draw.rect(screen, (255, 0, 0), basket_zone, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
