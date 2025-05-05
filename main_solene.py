import pygame

pygame.init()

# Game settings
DURATION = 30  # duration in seconds
screen = pygame.display.set_mode((600, 400))
font = pygame.font.Font(None, 50)

# Start Time
start_time = pygame.time.get_ticks()

running = True
while running:
    screen.fill((0, 0, 0))  # Black Background
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    # Check if the time is up
    if elapsed_time >= DURATION:
        print("⏳ Time's up! Game over !")
        running = False

    # Show remaining time
    time_text = font.render(f"Time left: {DURATION - elapsed_time}s", True, (255, 255, 255))
    screen.blit(time_text, (150, 180))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

