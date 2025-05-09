import pygame
import os
import math

class BallTrajectory:
    def __init__(self, image_folder, screen_width, screen_height, frame_count=15, frame_delay=3):
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(image_folder, f"pixil-frame-{i}.png")).convert_alpha(),
                (100, 100)  # largeur, hauteur agrandies
            )
            for i in range(1, frame_count + 1)
        ]
        self.frame_index = 0
        self.frame_delay = frame_delay
        self.frame_counter = 0

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Initial state
        self.reset()

    def reset(self):
        self.start_x = 100
        self.start_y = self.screen_height - 100
        self.x = self.start_x
        self.y = self.start_y
        self.t = 0
        self.angle = math.radians(60)  # default angle
        self.velocity = 20
        self.gravity = 0.5
        self.shooting = False
        self.animation_done = False
        self.frame_index = 0
        self.frame_counter = 0

    def update(self):
        if not self.shooting:
            return

        if self.animation_done:
            return

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.frame_index = len(self.frames) - 1

        self.t += 1
        self.x = self.start_x + self.velocity * self.t * math.cos(self.angle)
        self.y = self.start_y - (self.velocity * self.t * math.sin(self.angle) - self.gravity * self.t**2)

        if self.x > self.screen_width or self.y > self.screen_height:
            self.animation_done = True

    def draw(self, screen):
        frame = self.frames[self.frame_index]
        screen.blit(frame, (self.x, self.y))

    def launch(self):
        if not self.shooting:
            self.shooting = True
            self.t = 0
            self.x = self.start_x
            self.y = self.start_y
            self.animation_done = False
            self.frame_index = 0

    def adjust_angle(self, direction):
        angle_deg = math.degrees(self.angle)
        if direction == "up" and angle_deg < 85:
            angle_deg += 2
        elif direction == "down" and angle_deg > 30:
            angle_deg -= 2
        self.angle = math.radians(angle_deg)

    def adjust_velocity(self, direction):
        if direction == "right" and self.velocity < 40:
            self.velocity += 1
        elif direction == "left" and self.velocity > 5:
            self.velocity -= 1

    def draw_trajectory_dots(self, screen):
        if self.shooting:
            return  # Ne pas afficher pendant un tir

        # Prévisualisation de la trajectoire (pointillée)
        for i in range(5, 60, 2):  # commence à 5 pour ne pas dessiner sous la balle
            t = i
            dot_x = self.start_x + self.velocity * t * math.cos(self.angle)
            dot_y = self.start_y - (self.velocity * t * math.sin(self.angle) - self.gravity * t**2)

            if dot_x > self.screen_width or dot_y > self.screen_height:
                break

            pygame.draw.circle(screen, (255, 255, 255), (int(dot_x), int(dot_y)), 5)


pygame.init()
screen_width = 1200
screen_height = 675
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

ball = BallTrajectory("image/pixilart-frames-blue-ball", screen_width, screen_height)

font = pygame.font.Font(None, 40)

running = True
while running:
    screen.fill((0, 0, 0))

    # Mettre à jour et afficher la balle
    ball.update()
    ball.draw(screen)

    # Affiche les points de trajectoire
    ball.draw_trajectory_dots(screen)

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.adjust_angle("up")
            elif event.key == pygame.K_DOWN:
                ball.adjust_angle("down")
            elif event.key == pygame.K_LEFT:
                ball.adjust_velocity("left")
            elif event.key == pygame.K_RIGHT:
                ball.adjust_velocity("right")
            elif event.key == pygame.K_SPACE:
                ball.launch()

pygame.quit()