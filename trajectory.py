import pygame
import os
import math

def load_avatar(avatar):
    if avatar == 2:
        avatar = {
            "side": pygame.transform.scale(pygame.image.load("image/perso1side.png").convert_alpha(),(200,200)),
            "lance": pygame.transform.scale(pygame.image.load("image/perso1lance.png").convert_alpha(),(200,200)),
        }
    elif avatar == 1:
        avatar = {
            "side": pygame.transform.scale(pygame.image.load("image/pers2side.png").convert_alpha(),(200,200)),
            "lance": pygame.transform.scale(pygame.image.load("image/pers2lance.png").convert_alpha(),(200,200)),
        }
    elif avatar ==3:
        avatar = {
            "side": pygame.transform.scale(pygame.image.load("image/pers3side.png").convert_alpha(),(200,200)),
            "lance": pygame.transform.scale(pygame.image.load("image/pers3lance.png").convert_alpha(),(200,200)),
        }
    return avatar

def load_ball_frames(image_folder, frame_count=15, scale=(90, 100)):
    return [
        pygame.transform.scale(
            pygame.image.load(os.path.join(image_folder, f"frame{i}.png")).convert_alpha(),
            scale
        )
        for i in range(1, frame_count + 1)
    ]

def reset_ball_state(screen_width, screen_height):
    return {
        "frames": [],
        "frame_index": 0,
        "frame_delay": 3,
        "frame_counter": 0,
        "start_x": 100,
        "start_y": screen_height - 250,
        "x": 100,
        "y": screen_height - 300,
        "t": 0,
        "angle": math.radians(60),
        "velocity": 20,
        "gravity": 0.5,
        "shooting": False,
        "animation_done": False,
        "x_avatar" :0,
        "y_avatar" : screen_height - 220,
    }

def update_ball(state, screen_width, screen_height, image_folder):
    if not state["shooting"] or state["animation_done"]:
        return

    state["frame_counter"] += 1
    if state["frame_counter"] >= state["frame_delay"]:
        state["frame_counter"] = 0
        state["frame_index"] += 1
        if state["frame_index"] >= len(state["frames"]):
            state["frame_index"] = len(state["frames"]) - 1

    state["t"] += 1
    state["x"] = state["start_x"] + state["velocity"] * state["t"] * math.cos(state["angle"])
    state["y"] = state["start_y"] - (state["velocity"] * state["t"] * math.sin(state["angle"]) - state["gravity"] * state["t"]**2)

    if state["x"] > screen_width or state["y"] > screen_height:
        # Réinitialise totalement la balle
        new_state = reset_ball_state(screen_width, screen_height)
        new_state["frames"] = load_ball_frames(image_folder)
        state.clear()
        state.update(new_state)

def draw_ball(screen, state,avatar):
    if state["frames"]:
        frame = state["frames"][state["frame_index"]]
        screen.blit(frame, (state["x"], state["y"]))
    screen.blit(avatar["lance"], (state["x_avatar"], state["y_avatar"]))

def launch_ball(state):
    if not state["shooting"]:
        state["shooting"] = True
        state["t"] = 0
        state["x"] = state["start_x"]
        state["y"] = state["start_y"]
        state["animation_done"] = False
        state["frame_index"] = 0

def adjust_ball_angle(state, direction):
    angle_deg = math.degrees(state["angle"])
    if direction == "up" and angle_deg < 85:
        angle_deg += 2
    elif direction == "down" and angle_deg > 30:
        angle_deg -= 2
    state["angle"] = math.radians(angle_deg)

def adjust_ball_velocity(state, direction):
    if direction == "right" and state["velocity"] < 40:
        state["velocity"] += 1
    elif direction == "left" and state["velocity"] > 5:
        state["velocity"] -= 1

def draw_trajectory_dots(screen, state, screen_width, screen_height):
    if state["shooting"]:
        return
    for i in range(5, 60, 2):
        t = i
        dot_x = state["start_x"] + state["velocity"] * t * math.cos(state["angle"])
        dot_y = state["start_y"] - (state["velocity"] * t * math.sin(state["angle"]) - state["gravity"] * t**2)
        if dot_x > screen_width or dot_y > screen_height:
            break
        pygame.draw.circle(screen, (255, 255, 255), (int(dot_x), int(dot_y)), 5)