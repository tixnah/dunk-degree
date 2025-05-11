# check_events.py
import pygame
import time
from trajectory import launch_ball, adjust_ball_angle, adjust_ball_velocity
import sound_manager

# ... (rest of the existing imports and global variables) ...
menu_bg_raw = pygame.image.load("image/menu.png");
guide_bg_raw = pygame.image.load("image/guide.png")
game_bg_raw = pygame.image.load("image/background.png");
parameter_on_bg_raw = pygame.image.load("image/parameter_on.png")
parameter_off_bg_raw = pygame.image.load("image/parameter_off.png");
violet_ball_img_raw = pygame.image.load("image_menu/violet_ball.png")
blue_ball_img_raw = pygame.image.load("image_menu/blue_ball.png");
orange_ball_img_raw = pygame.image.load("image_menu/orange_ball.png")
selected_violet_ball_img_raw = pygame.image.load("image_menu/selected_violet_ball.png");
selected_blue_ball_img_raw = pygame.image.load("image_menu/selected_blue_ball.png")
selected_orange_ball_img_raw = pygame.image.load("image_menu/selected_orange_ball.png");
avatar_1_img_raw = pygame.image.load("image_menu/avatar_1.png")
avatar_2_img_raw = pygame.image.load("image_menu/avatar_2.png");
avatar_3_img_raw = pygame.image.load("image_menu/avatar_3.png")
selected_avatar_1_img_raw = pygame.image.load("image_menu/selected_avatar_1.png");
selected_avatar_2_img_raw = pygame.image.load("image_menu/selected_avatar_2.png")
selected_avatar_3_img_raw = pygame.image.load("image_menu/selected_avatar_3.png")

menu_bg, guide_bg, game_bg, parameter_on_bg, parameter_off_bg = [None] * 5
violet_ball_img, blue_ball_img, orange_ball_img = [None] * 3
selected_violet_ball_img, selected_blue_ball_img, selected_orange_ball_img = [None] * 3
avatar_1_img, avatar_2_img, avatar_3_img = [None] * 3
selected_avatar_1_img, selected_avatar_2_img, selected_avatar_3_img = [None] * 3


def init_check_events_assets():
    global menu_bg, guide_bg, game_bg, parameter_on_bg, parameter_off_bg, violet_ball_img, blue_ball_img, orange_ball_img
    global selected_violet_ball_img, selected_blue_ball_img, selected_orange_ball_img, avatar_1_img, avatar_2_img, avatar_3_img
    global selected_avatar_1_img, selected_avatar_2_img, selected_avatar_3_img
    menu_bg = menu_bg_raw.convert();
    guide_bg = guide_bg_raw.convert();
    game_bg = game_bg_raw.convert()
    parameter_on_bg = parameter_on_bg_raw.convert();
    parameter_off_bg = parameter_off_bg_raw.convert()
    violet_ball_img = violet_ball_img_raw.convert_alpha();
    blue_ball_img = blue_ball_img_raw.convert_alpha();
    orange_ball_img = orange_ball_img_raw.convert_alpha()
    selected_violet_ball_img = selected_violet_ball_img_raw.convert_alpha();
    selected_blue_ball_img = selected_blue_ball_img_raw.convert_alpha();
    selected_orange_ball_img = selected_orange_ball_img_raw.convert_alpha()
    avatar_1_img = avatar_1_img_raw.convert_alpha();
    avatar_2_img = avatar_2_img_raw.convert_alpha();
    avatar_3_img = avatar_3_img_raw.convert_alpha()
    selected_avatar_1_img = selected_avatar_1_img_raw.convert_alpha();
    selected_avatar_2_img = selected_avatar_2_img_raw.convert_alpha();
    selected_avatar_3_img = selected_avatar_3_img_raw.convert_alpha()


start_button_rect = pygame.Rect(132, 556, 106, 35);
guide_button_rect = pygame.Rect(382, 556, 119, 35)
parameter_button_rect = pygame.Rect(686, 556, 119, 35);
quit_menu_button_rect = pygame.Rect(963, 556, 79, 35)
return_menu_button_rect = pygame.Rect(830, 529, 237, 66);
music_on_button_rect = pygame.Rect(829, 189, 76, 41)
music_off_button_rect = pygame.Rect(1002, 189, 76, 41);
violet_ball_button_rect = pygame.Rect(651, 370, 115, 102)
blue_ball_button_rect = pygame.Rect(824, 370, 115, 102);
orange_ball_button_rect = pygame.Rect(996, 370, 115, 102)
avatar_1_button_rect = pygame.Rect(89, 243, 115, 178);
avatar_2_button_rect = pygame.Rect(266, 243, 115, 178)
avatar_3_button_rect = pygame.Rect(449, 243, 115, 178);
quit_game_button_rect = pygame.Rect(1001, 20, 172, 42)

_internal_running = True;
_internal_game_launched = False;
_internal_avatar = 1
_internal_ball_path = "image/frames-purple-ball"
_music_enabled = True
_internal_current_screen = "menu"
_events_for_game_event = []

music_status_for_main = _music_enabled


# NEW FUNCTION to be called by main.py when game ends internally
def set_game_ended_from_main():
    global _internal_game_launched, _internal_current_screen
    _internal_game_launched = False
    _internal_current_screen = "menu"
    pygame.display.set_caption(f"Dunk & Degree - Menu")  # Optional: update caption immediately


def menu_event(SCREEN_WIDTH_UNUSED, SCREEN_HEIGHT_UNUSED, screen_surface_UNUSED):
    global _internal_running, _internal_current_screen, _internal_game_launched, _internal_avatar
    global _internal_ball_path, _music_enabled, _events_for_game_event, music_status_for_main
    pos = None;
    _events_for_game_event = pygame.event.get()

    for event in _events_for_game_event:
        if event.type == pygame.QUIT: _internal_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Only consider clicks if not in game, or if it's the quit game button during game
            if not _internal_game_launched or (
                    _internal_game_launched and quit_game_button_rect.collidepoint(event.pos)):
                pos = event.pos
            # This line was a bit complex, simplified above. Original:
            # if _internal_current_screen != "game" or not _internal_game_launched:
            #     pos = event.pos
            # elif _internal_current_screen == "game" and _internal_game_launched:
            #     if quit_game_button_rect.collidepoint(event.pos):
            #         pos = event.pos

        if pos is not None:
            prev_screen = _internal_current_screen
            if _internal_current_screen == "menu":
                if start_button_rect.collidepoint(pos):
                    _internal_current_screen = "game";
                    _internal_game_launched = True
                elif guide_button_rect.collidepoint(pos):
                    _internal_current_screen = "guide"
                elif parameter_button_rect.collidepoint(pos):
                    _internal_current_screen = "parameter_on" if _music_enabled else "parameter_off"
                elif quit_menu_button_rect.collidepoint(pos):
                    _internal_running = False
            elif _internal_current_screen == "guide":
                if return_menu_button_rect.collidepoint(pos): _internal_current_screen = "menu"
            elif _internal_current_screen in ["parameter_on", "parameter_off"]:
                if return_menu_button_rect.collidepoint(pos): _internal_current_screen = "menu"

                if _music_enabled and music_off_button_rect.collidepoint(pos):
                    _music_enabled = False
                    sound_manager.stop_music()
                    _internal_current_screen = "parameter_off"
                    # print("Music OFF") # Debug
                elif not _music_enabled and music_on_button_rect.collidepoint(pos):
                    _music_enabled = True
                    # Music will be handled by main.py's play_appropriate_music logic
                    _internal_current_screen = "parameter_on"
                    # print("Music ON") # Debug

                if avatar_1_button_rect.collidepoint(pos):
                    _internal_avatar = 1
                elif avatar_2_button_rect.collidepoint(pos):
                    _internal_avatar = 2
                elif avatar_3_button_rect.collidepoint(pos):
                    _internal_avatar = 3
                if violet_ball_button_rect.collidepoint(pos):
                    _internal_ball_path = "image/frames-purple-ball"
                elif blue_ball_button_rect.collidepoint(pos):
                    _internal_ball_path = "image/frames-blue-ball"
                elif orange_ball_button_rect.collidepoint(pos):
                    _internal_ball_path = "image/frames-orange-ball"

            # This case handles the "Quit Game" button clicked from the game screen overlay
            elif _internal_current_screen == "game" and _internal_game_launched:  # Check _internal_game_launched to be sure
                if quit_game_button_rect.collidepoint(pos):
                    _internal_current_screen = "menu"
                    _internal_game_launched = False

            if prev_screen != _internal_current_screen and _internal_current_screen != "game":  # Avoid changing caption if going to game
                new_caption = f"Dunk & Degree - {_internal_current_screen.replace('_', ' ').title()}"
                pygame.display.set_caption(new_caption)
            elif _internal_current_screen == "game" and _internal_game_launched:
                pygame.display.set_caption("Dunk & Degree - Playing")

            pos = None

    music_status_for_main = _music_enabled
    return _internal_running, _internal_game_launched, _internal_ball_path, _internal_avatar, _internal_current_screen, music_status_for_main


def show_img(s, ui_state_for_background):
    # Parameter screen background depends on _music_enabled and the ui_state
    if ui_state_for_background == "parameter_on":  # Intended state is ON
        s.blit(parameter_on_bg if _music_enabled else parameter_off_bg, (0, 0))
    elif ui_state_for_background == "parameter_off":  # Intended state is OFF
        s.blit(parameter_off_bg if not _music_enabled else parameter_on_bg, (0, 0))
    elif ui_state_for_background == "menu" and menu_bg:
        s.blit(menu_bg, (0, 0))
    elif ui_state_for_background == "guide" and guide_bg:
        s.blit(guide_bg, (0, 0))
    elif ui_state_for_background == "game" and game_bg:
        s.blit(game_bg, (0, 0))


def show_overlay(s, ui_state_from_menu_event, avatar_id, ball_path):
    if ui_state_from_menu_event in ["parameter_on", "parameter_off"]:
        if not avatar_1_img: return  # Ensure assets are loaded

        current_avatar_display_tuple = (selected_avatar_1_img, avatar_2_img, avatar_3_img)
        if avatar_id == 2:
            current_avatar_display_tuple = (avatar_1_img, selected_avatar_2_img, avatar_3_img)
        elif avatar_id == 3:
            current_avatar_display_tuple = (avatar_1_img, avatar_2_img, selected_avatar_3_img)

        s.blit(current_avatar_display_tuple[0], (66, 238));
        s.blit(current_avatar_display_tuple[1], (239, 238));
        s.blit(current_avatar_display_tuple[2], (411, 238))

        current_ball_display_tuple = (selected_violet_ball_img, blue_ball_img, orange_ball_img)
        if ball_path == "image/frames-blue-ball":
            current_ball_display_tuple = (violet_ball_img, selected_blue_ball_img, orange_ball_img)
        elif ball_path == "image/frames-orange-ball":
            current_ball_display_tuple = (violet_ball_img, blue_ball_img, selected_orange_ball_img)

        s.blit(current_ball_display_tuple[0], (636, 354));
        s.blit(current_ball_display_tuple[1], (810, 354));
        s.blit(current_ball_display_tuple[2], (985, 354))


def game_event(ball_state, current_game_play_state_from_main):
    global _events_for_game_event  # Use the events captured by menu_event

    # Only process game inputs if the game is in 'playing' state
    if current_game_play_state_from_main != "playing":
        _events_for_game_event = []  # Clear events if not in playing state to avoid stale inputs
        return True

    running_status = True  # Default to true, could be changed by e.g. ESC key if implemented
    for e in _events_for_game_event:
        # pygame.QUIT is handled in menu_event, but good to have a safeguard
        if e.type == pygame.QUIT:
            running_status = False
            break
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                launch_ball(ball_state)
            elif e.key == pygame.K_UP:
                adjust_ball_angle(ball_state, "up")
            elif e.key == pygame.K_DOWN:
                adjust_ball_angle(ball_state, "down")
            elif e.key == pygame.K_LEFT:
                adjust_ball_velocity(ball_state, "left")
            elif e.key == pygame.K_RIGHT:
                adjust_ball_velocity(ball_state, "right")
            # Example: if e.key == pygame.K_ESCAPE: running_status = False # To quit game via ESC

    _events_for_game_event = []  # Clear events after processing
    return running_status