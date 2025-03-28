import pygame

pygame.init()

# Game settings
DURATION = 45  # duration in seconds
screen_width, screen_height = 1200, 675
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dunk & Degree")

# Load assets
background = pygame.image.load("background.png")
basket = pygame.image.load("basket.png")
basket = pygame.transform.scale(basket, (400, 350))
font = pygame.font.Font(None, 50)

# Start time
start_time = pygame.time.get_ticks()

running = True


def check_event():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


while running:
    check_event()

    # Draw images
    screen.blit(background, (0, 0))
    screen.blit(basket, (850, 50))

    # Timer
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    remaining_time = max(0, DURATION - elapsed_time)

    # Show remaining time
    time_text = font.render(f"Remaining Time: {remaining_time}s", True, (255, 255, 255))
    screen.blit(time_text, (40, 30))

    pygame.display.flip()  # Refresh screen

    # Check if time is up
    if remaining_time <= 0:
        print("⏳ Time's up! Game over!")
        running = False

pygame.quit()
