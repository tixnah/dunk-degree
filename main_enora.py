import pygame
import random



#  Initialisation of Pygame
pygame.init()



            #Nour's program
#Screen
screen_width = 1200
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Dunk & Degree")



#Basket's image
basket_img = pygame.image.load("basket.png").convert_alpha()
basket_img = pygame.transform.scale(basket_img, (80,50))

#Ball's image
ball_img = pygame.image.load("ball_orange.png").convert_alpha()
ball_img = pygame.transform.scale(ball_img, (30,30))

#Initials positions
ball_x, ball_y = screen_width// 2, screen_height - 50  #Initial position of the ball
basket_x, basket_y = screen_width // 2, 100   #Initial position of the basket
ball_speed_y = -10     #Speed of ball when it up
ball_in_air = False    #Verify if the ball is in air or not


#Parameter's level
difficulty_levels={
    "Easy":{"speed":0, "modes":[0]},
    "Normal":{"speed": 2,"modes":[1,2,3]},
    "Intermediate":{"speed":4, "modes":[1,2,3,4,5]},
    "Difficult":{"speed": 6, "modes":[1,2,3,4,5]},
    "Expert":{"speed":8, "modes":[6]}
}


difficulty = "Easy" #To modify for changing the difficulty
basket_mode = random.choice(difficulty_levels[difficulty]["modes"])
basket_speed = difficulty_levels[difficulty]["speed"]
basket_dx,basket_dy = basket_speed, basket_speed







def move_basket():
    global basket_x, basket_y, basket_dx, basket_dy, basket_speed
    if difficulty == "Expert":
        basket_speed += 0.01 #Augmentation of the velocity with the time
        basket_x = basket_dy = int(basket_speed)
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




def check_collision ():
    global ball_x, ball_y, ball_in_air
    if basket_x < ball_x < ball_x + 80 and basket_y < ball_y < basket_y + 50:
        print("Basket reused!")
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

    screen.blit(basket_img, (basket_x, basket_y))
    screen.blit(ball_img, (ball_x, ball_y))

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()