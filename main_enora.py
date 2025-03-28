import pygame
import random
import time
import main_nour



#  Initialisation of Pygame
pygame.init()


#Nour's program

#Screen
screen_width = 1200
screen_height = 750
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



#Ball's image
ball_img = pygame.image.load("ball_violet.png").convert_alpha()
ball_img = pygame.transform.scale(ball_img, (90,90))



#Initials positions
ball_x, ball_y = screen_width// 10, screen_height - 50  #Initial position of the ball
# basket_x, basket_y = screen_width//2, 100   #Initial position of the basket
ball_speed_y = -10     #Speed of ball when it up
ball_in_air = False    #Verify if the ball is in air or not


#Score
score = 0
difficulty_levels_order = ["Easy", "Normal", "Intermediate", "Difficult"]
current_level_index = 0


#Parameter's level
difficulty_levels = {
    "Easy": {"level" : [1, 2, 3], "speed": 0, "modes": [0]},
    "Normal": {"level" : [4, 5, 6], "speed": 2, "modes": [1, 2, 3]},
    "Intermediate": {"level" : [7, 8, 9], "speed": 4, "modes": [1, 2, 3, 4, 5]},
    "Difficult": {"level": [10, 11, 12], "speed": 6, "modes": [1, 2, 3, 4, 5]},
}

difficulty = "Easy"  # Modify for change the difficulty
basket_mode = random.choice(difficulty_levels[difficulty]["modes"])
basket_speed = difficulty_levels[difficulty]["speed"]
basket_dx, basket_dy = basket_speed, basket_speed



# move basket

def move_basket():
    global basket_x, basket_y, basket_dx, basket_dy, basket_speed

    #left-right
    if basket_mode == 1:
        basket_x += basket_dx
        if basket_x <= 0 or basket_x >= screen_width - 80:
            basket_dx *= -1

    #up-done
    elif basket_mode == 2:
        basket_y += basket_dy
        if basket_y <= 50 or basket_y >= screen_height // 2:
            basket_dy += -1

    #every directions
    elif basket_mode == 3:
        basket_x += basket_dx
        basket_y += basket_dy
        if basket_x <=0 or basket_x >= screen_width - 80:
            basket_dx *= -1
        if basket_y <= 50 or basket_y >= screen_height // 2:
            basket_dy *= -1

    #diagonals
    elif basket_mode == 4:
        basket_x += basket_dx
        basket_y += basket_y
        if basket_x <= 0 or basket_y >= screen_width - 80:
            basket_dx *= -1
        if basket_y <= 50 or basket_y >= screen_height // 2:
           basket_dy *= -1


time = 0

def check_collision ():
    global ball_x, ball_y, ball_in_air,score, difficulty, current_level_index, time

    if basket_x < ball_x < ball_x + 80 and basket_y < ball_y < basket_y + 50:
        score += 1 #Add 1 point
        print(f"Basket reused! Score: {score}")

        if score in [10, 30, 60, 100, 150] and current_level_index < len(difficulty_levels_order)-1:
            current_level_index += 1
            difficulty = difficulty_levels_order[current_level_index]
            print(f"New level: {difficulty}")
            if score == 150:
                print ("Bravo !!")
                time = time.sleep(10)
                print ("Wait... ")
                time = time.sleep(5)
                print ("New level ? :D ")

        ball_x, ball_y = screen_width//2, screen_height - 50
        return True
    return False

running = True
while running :
    #screen.fill(difficulty_levels [difficulty]["color"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not ball_in_air:
                ball_in_air = True

    if ball_in_air:
        ball_y += ball_speed_y
        if ball_y < 0 or check_collision():
            ball_in_air = False
            ball_x, ball_y = screen_width // 2, screen_height - 50

    move_basket ()

    #screen.blit(basket_img, (basket_x, basket_y))
    screen.blit(ball_img, (ball_x, ball_y))

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
