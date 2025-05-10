import pygame
import time
from trajectory import launch_ball, adjust_ball_angle, adjust_ball_velocity

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
_internal_ball_path = "image/frames-purple-ball";
_internal_music = True;
_internal_current_screen = "menu"
_events_for_game_event = []


def menu_event(SCREEN_WIDTH_UNUSED, SCREEN_HEIGHT_UNUSED, screen_surface_UNUSED):
    global _internal_running, _internal_current_screen, _internal_game_launched, _internal_avatar, _internal_ball_path, _internal_music, _events_for_game_event
    pos = None;
    _events_for_game_event = pygame.event.get()

    for event in _events_for_game_event:
        if event.type == pygame.QUIT: _internal_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if _internal_current_screen != "game" or not _internal_game_launched:
                pos = event.pos
            elif _internal_current_screen == "game" and _internal_game_launched:
                if quit_game_button_rect.collidepoint(event.pos):
                    pos = event.pos

        if pos is not None:
            prev_screen = _internal_current_screen
            if _internal_current_screen == "menu":
                if start_button_rect.collidepoint(pos):
                    _internal_current_screen = "game";_internal_game_launched = True
                elif guide_button_rect.collidepoint(pos):
                    _internal_current_screen = "guide"
                elif parameter_button_rect.collidepoint(pos):
                    _internal_current_screen = "parameter_on" if _internal_music else "parameter_off"
                elif quit_menu_button_rect.collidepoint(pos):
                    _internal_running = False
            elif _internal_current_screen == "guide":
                if return_menu_button_rect.collidepoint(pos): _internal_current_screen = "menu"
            elif _internal_current_screen in ["parameter_on", "parameter_off"]:
                if return_menu_button_rect.collidepoint(pos): _internal_current_screen = "menu"
                if _internal_current_screen == "parameter_on" and music_off_button_rect.collidepoint(pos):
                    _internal_music = False;_internal_current_screen = "parameter_off"
                elif _internal_current_screen == "parameter_off" and music_on_button_rect.collidepoint(pos):
                    _internal_music = True;_internal_current_screen = "parameter_on"
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
            elif _internal_current_screen == "game":
                if quit_game_button_rect.collidepoint(
                    pos): _internal_current_screen = "menu";_internal_game_launched = False

            if prev_screen != _internal_current_screen:
                new_caption = f"Dunk & Degree - {_internal_current_screen.replace('_', ' ').title()}"
                pygame.display.set_caption(new_caption)
            pos = None
    return _internal_running, _internal_game_launched, _internal_ball_path, _internal_avatar, _internal_current_screen


def show_img(s, ui_state_for_background):
    if ui_state_for_background == "menu" and menu_bg:
        s.blit(menu_bg, (0, 0))
    elif ui_state_for_background == "guide" and guide_bg:
        s.blit(guide_bg, (0, 0))
    elif ui_state_for_background == "game" and game_bg:
        s.blit(game_bg, (0, 0))
    elif ui_state_for_background == "parameter_on" and parameter_on_bg:
        s.blit(parameter_on_bg, (0, 0))
    elif ui_state_for_background == "parameter_off" and parameter_off_bg:
        s.blit(parameter_off_bg, (0, 0))


def show_overlay(s, ui_state_from_menu_event, avatar_id, ball_path):
    if ui_state_from_menu_event in ["parameter_on", "parameter_off"]:
        if not avatar_1_img: return
        a1, a2, a3 = (selected_avatar_1_img, avatar_2_img, avatar_3_img) if avatar_id == 1 else (
        avatar_1_img, selected_avatar_2_img, avatar_3_img) if avatar_id == 2 else (
        avatar_1_img, avatar_2_img, selected_avatar_3_img)
        s.blit(a1, (66, 238));
        s.blit(a2, (239, 238));
        s.blit(a3, (411, 238))
        b1, b2, b3 = (
        selected_violet_ball_img, blue_ball_img, orange_ball_img) if ball_path == "image/frames-purple-ball" else (
        violet_ball_img, selected_blue_ball_img, orange_ball_img) if ball_path == "image/frames-blue-ball" else (
        violet_ball_img, blue_ball_img, selected_orange_ball_img)
        s.blit(b1, (636, 354));
        s.blit(b2, (810, 354));
        s.blit(b3, (985, 354))


def game_event(ball_state, current_game_play_state_from_main):
    global _events_for_game_event
    if current_game_play_state_from_main != "playing":
        _events_for_game_event = []
        return True
    running_status = True
    for e in _events_for_game_event:
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
    _events_for_game_event = []
    return running_status