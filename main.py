import pygame
import time
import os

pygame.init()

from check_events import menu_event, game_event, show_img, show_overlay, init_check_events_assets
from level import basket_hoop, get_basket_rect, difficulty, init_level_assets, reset_basket_position_for_level
from trajectory import (reset_ball_state, load_ball_frames, load_avatar, update_ball,
                        draw_trajectory_dots, draw_ball)
import sound_manager

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dunk & Degree")

init_check_events_assets()
init_level_assets(SCREEN_WIDTH, SCREEN_HEIGHT)
sound_manager.init_mixer()

winner_screen_image = None
game_over_lose_screen_image = None
try:
    winner_screen_image = pygame.image.load("image/winner_screen.jpg").convert()
    winner_screen_image = pygame.transform.scale(winner_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Erreur chargement image victoire: {e}")
    winner_screen_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT));
    winner_screen_image.fill((20, 100, 20))
    fb_font_w = pygame.font.Font(None, 50);
    fb_text_w = fb_font_w.render("FELICITATIONS !", True, (255, 255, 255))
    fb_rect_w = fb_text_w.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2));
    winner_screen_image.blit(fb_text_w, fb_rect_w)
try:
    game_over_lose_screen_image = pygame.image.load("image/game_over_screen.jpg").convert()
    game_over_lose_screen_image = pygame.transform.scale(game_over_lose_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error as e:
    print(f"Erreur chargement image Game Over: {e}")
    game_over_lose_screen_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT));
    game_over_lose_screen_image.fill((100, 20, 20))
    fb_font_go = pygame.font.Font(None, 80);
    fb_text_go = fb_font_go.render("GAME OVER", True, (255, 255, 255))
    fb_rect_go = fb_text_go.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50));
    game_over_lose_screen_image.blit(fb_text_go, fb_rect_go)

ball_state = reset_ball_state(SCREEN_WIDTH, SCREEN_HEIGHT)
running = True;
game_launched_from_menu = False;
game_assets_loaded = False
GAME_STATE_MENU = "menu_ui_state";
GAME_STATE_PLAYING = "playing";
GAME_STATE_LEVEL_TRANSITION = "level_transition"
GAME_STATE_GAME_OVER_TIME = "game_over_time";
GAME_STATE_GAME_OVER_WIN = "game_over_win"
current_game_play_state = GAME_STATE_MENU
difficulty_selector = 0;
level_value = 0;
score = 0
current_ball_path = "image/frames-purple-ball";
current_avatar_id = 1
selected_avatar_imgs = None;
clock = pygame.time.Clock()
LEVEL_DURATION = 30;
level_start_time = 0;
time_remaining = LEVEL_DURATION
basket_scored_this_level = False;
LEVEL_TRANSITION_DURATION = 5000;
level_transition_start_time = 0
GAME_OVER_MESSAGE_DURATION = 3000;
game_over_time_display_start = 0
HOOP_OFFSET_X = 55;
HOOP_OFFSET_Y = 45;
HOOP_WIDTH = 90;
HOOP_HEIGHT = 30
score_font = pygame.font.Font(None, 60);
timer_font = pygame.font.Font(None, 60)
message_font = pygame.font.Font(None, 80);
small_message_font = pygame.font.Font(None, 40)
final_score_font = pygame.font.Font(None, 70)
basket_current_x = 0;
basket_current_y = 0
ui_screen_state_for_background = "menu";
ui_state_from_menu_event = "menu"
LEVEL_TRANSITION_IMAGE_PATH = "image/level_screens/";
level_transition_images = {};
current_level_transition_image = None


def get_global_level_number(cur_diff_sel, cur_lvl_val):
    gl = 0;
    if cur_diff_sel == 0:
        gl = cur_lvl_val + 1
    elif cur_diff_sel == 1:
        gl = 3 + cur_lvl_val + 1
    elif cur_diff_sel == 2:
        gl = 3 + 3 + cur_lvl_val + 1
    elif cur_diff_sel == 3:
        gl = 3 + 3 + 5 + cur_lvl_val + 1
    return gl


def load_level_transition_image(gl_lvl_num):
    global level_transition_images
    if gl_lvl_num in level_transition_images: return level_transition_images[gl_lvl_num]
    img_fname = f"level_{gl_lvl_num}.jpg";
    full_path = os.path.join(LEVEL_TRANSITION_IMAGE_PATH, img_fname)
    try:
        img = pygame.image.load(full_path).convert(); level_transition_images[gl_lvl_num] = img; return img
    except pygame.error as e:
        print(f"Err load img trans {full_path}:{e}");
        fb = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT));
        fb.fill((70, 70, 170))
        txt_s = small_message_font.render(f"Img Niv {gl_lvl_num} Manquante", True, (255, 255, 255));
        txt_r = txt_s.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2));
        fb.blit(txt_s, txt_r)
        level_transition_images[gl_lvl_num] = fb;
        return fb


def play_appropriate_music():
    global difficulty_selector, current_game_play_state
    target_music_key = None;
    loops = -1;
    volume = 0.5
    if current_game_play_state == GAME_STATE_MENU:
        target_music_key = "menu"
    elif current_game_play_state == GAME_STATE_PLAYING or current_game_play_state == GAME_STATE_LEVEL_TRANSITION:
        if difficulty_selector == 0:
            target_music_key = "palier1_easy"
        elif difficulty_selector == 1:
            target_music_key = "palier2_normal"
        elif difficulty_selector == 2:
            target_music_key = "palier3_intermediate"
        elif difficulty_selector == 3:
            target_music_key = "palier4_difficult"
    elif current_game_play_state == GAME_STATE_GAME_OVER_WIN:
        target_music_key = "score_fin_win"; loops = 0
    elif current_game_play_state == GAME_STATE_GAME_OVER_TIME:
        target_music_key = "game_over_lose"; loops = 0
    if target_music_key and not sound_manager.is_playing(target_music_key):
        sound_manager.play_music(target_music_key, loops=loops, volume=volume)
    elif not target_music_key and current_game_play_state != GAME_STATE_LEVEL_TRANSITION:
        sound_manager.stop_music()


def start_new_level_setup():
    global basket_scored_this_level, ball_state, current_game_play_state, game_assets_loaded, current_ball_path
    global difficulty_selector, level_value, current_level_transition_image, level_transition_start_time
    basket_scored_this_level = False;
    ball_state = reset_ball_state(SCREEN_WIDTH, SCREEN_HEIGHT)
    reset_basket_position_for_level(difficulty_selector, level_value, SCREEN_WIDTH, SCREEN_HEIGHT)
    if game_assets_loaded and (not ball_state["frames"] or ball_state["frames"] == []):
        ball_state["frames"] = load_ball_frames(current_ball_path)
        if not ball_state["frames"]: print("ERR FATAL: Rechargement frames balle.")
    gl_lvl_num = get_global_level_number(difficulty_selector, level_value)
    current_level_transition_image = load_level_transition_image(gl_lvl_num)
    current_game_play_state = GAME_STATE_LEVEL_TRANSITION;
    level_transition_start_time = pygame.time.get_ticks()
    play_appropriate_music()


def advance_to_next_challenge():
    global level_value, difficulty_selector, current_game_play_state
    max_lvl = 3 if difficulty[difficulty_selector] in ["Easy", "Normal"] else 5
    if level_value < max_lvl - 1:
        level_value += 1;start_new_level_setup()
    else:
        if difficulty_selector < len(difficulty) - 1:
            difficulty_selector += 1;level_value = 0;start_new_level_setup()
        else:
            print("JEU COMPLETÉ!");current_game_play_state = GAME_STATE_GAME_OVER_WIN; play_appropriate_music()


def display_centered_message(txt, fnt, col=(255, 255, 255), y_off=0, aa=True):
    s = fnt.render(txt, aa, col);
    r = s.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_off));
    screen.blit(s, r)


play_appropriate_music()

while running:
    previous_game_launched_state = game_launched_from_menu
    new_running, new_game_launched_flag_from_menu, new_bpath, new_aid, ui_state_from_menu_event = menu_event(
        SCREEN_WIDTH, SCREEN_HEIGHT, screen)
    running = new_running;
    current_ball_path = new_bpath;
    current_avatar_id = new_aid
    game_launched_from_menu = new_game_launched_flag_from_menu

    if game_launched_from_menu != previous_game_launched_state:
        if game_launched_from_menu:
            ui_screen_state_for_background = "game";
            game_assets_loaded = False;
            score = 0;
            level_value = 0;
            difficulty_selector = 0
            start_new_level_setup()
        else:
            ui_screen_state_for_background = "menu";
            game_assets_loaded = False;
            selected_avatar_imgs = None
            current_game_play_state = GAME_STATE_MENU;
            play_appropriate_music()
            if "frames" in ball_state: ball_state["frames"] = []
    elif not game_launched_from_menu and current_game_play_state != GAME_STATE_MENU:
        ui_screen_state_for_background = "menu";
        current_game_play_state = GAME_STATE_MENU;
        play_appropriate_music()
    elif not game_launched_from_menu:
        ui_screen_state_for_background = ui_state_from_menu_event
        if sound_manager.current_music_key != "menu": play_appropriate_music()

    if current_game_play_state not in [GAME_STATE_GAME_OVER_WIN, GAME_STATE_GAME_OVER_TIME]:
        show_img(screen, ui_screen_state_for_background)
    show_overlay(screen, ui_state_from_menu_event, current_avatar_id, current_ball_path)

    if game_launched_from_menu:
        if not game_assets_loaded and current_game_play_state not in [GAME_STATE_LEVEL_TRANSITION,
                                                                      GAME_STATE_GAME_OVER_TIME,
                                                                      GAME_STATE_GAME_OVER_WIN]:
            ball_state["frames"] = load_ball_frames(current_ball_path);
            selected_avatar_imgs = load_avatar(current_avatar_id)
            if not selected_avatar_imgs or not ball_state["frames"]:
                print("ERR FATAL: Assets jeu NI.");running = False
            else:
                game_assets_loaded = True

        if game_assets_loaded or current_game_play_state in [GAME_STATE_LEVEL_TRANSITION, GAME_STATE_GAME_OVER_TIME,
                                                             GAME_STATE_GAME_OVER_WIN]:
            if current_game_play_state == GAME_STATE_PLAYING:
                current_palier_music_key = f"palier{difficulty_selector + 1}_{difficulty[difficulty_selector].lower().replace(' ', '_')}"
                if difficulty_selector == 0:
                    current_palier_music_key = "palier1_easy"
                elif difficulty_selector == 1:
                    current_palier_music_key = "palier2_normal"
                elif difficulty_selector == 2:
                    current_palier_music_key = "palier3_intermediate"
                elif difficulty_selector == 3:
                    current_palier_music_key = "palier4_difficult"
                if not sound_manager.is_playing(current_palier_music_key): play_appropriate_music()

                el_time = time.time() - level_start_time;
                time_remaining = max(0, LEVEL_DURATION - int(el_time))
                basket_current_x, basket_current_y = basket_hoop(screen, difficulty_selector, level_value, SCREEN_WIDTH,
                                                                 SCREEN_HEIGHT)
                update_ball(ball_state, SCREEN_WIDTH, SCREEN_HEIGHT, current_ball_path)
                if selected_avatar_imgs: draw_ball(screen, ball_state, selected_avatar_imgs)
                hoop_info = {"x": basket_current_x + HOOP_OFFSET_X, "y": basket_current_y + HOOP_OFFSET_Y,
                             "width": HOOP_WIDTH, "height": HOOP_HEIGHT}
                draw_trajectory_dots(screen, ball_state, SCREEN_WIDTH, SCREEN_HEIGHT, hoop_info)
                if ball_state["shooting"] and not ball_state["scored_this_throw"]:
                    if ball_state["frames"] and len(ball_state["frames"]) > 0:
                        b_rect = ball_state["frames"][0].get_rect(topleft=(ball_state["x"], ball_state["y"]))
                        h_rect = pygame.Rect(hoop_info["x"], hoop_info["y"], hoop_info["width"], hoop_info["height"])
                        if h_rect.collidepoint(b_rect.centerx, b_rect.centery) and ball_state.get("vy_physics",
                                                                                                  1) < -0.01:
                            score += 1;
                            ball_state["scored_this_throw"] = True;
                            basket_scored_this_level = True
                if time_remaining <= 0:
                    if basket_scored_this_level:
                        advance_to_next_challenge()
                    else:
                        current_game_play_state = GAME_STATE_GAME_OVER_TIME; game_over_time_display_start = pygame.time.get_ticks(); play_appropriate_music()
                running = game_event(ball_state, current_game_play_state)
                s_surf = score_font.render(f"Score: {score}", True, (255, 255, 255));
                screen.blit(s_surf, (10, 10))
                gl_lvl = get_global_level_number(difficulty_selector, level_value);
                lvl_txt = f"Niveau {gl_lvl}"
                lvl_s = score_font.render(lvl_txt, True, (255, 255, 255));
                lvl_r = lvl_s.get_rect(midtop=(SCREEN_WIDTH // 2, 10));
                screen.blit(lvl_s, lvl_r)
                t_surf = timer_font.render(f"Temps: {time_remaining}", True, (255, 255, 0));
                t_r = t_surf.get_rect(topright=(SCREEN_WIDTH - 10, 10));
                screen.blit(t_surf, t_r)

            elif current_game_play_state == GAME_STATE_LEVEL_TRANSITION:
                if current_level_transition_image:
                    screen.blit(current_level_transition_image, (0, 0))
                else:
                    display_centered_message(f"NIVEAU {get_global_level_number(difficulty_selector, level_value)}",
                                             message_font, (200, 200, 0), -50)
                cur_ticks = pygame.time.get_ticks()
                if cur_ticks - level_transition_start_time >= LEVEL_TRANSITION_DURATION:
                    level_start_time = time.time();
                    time_remaining = LEVEL_DURATION;
                    basket_scored_this_level = False
                    current_game_play_state = GAME_STATE_PLAYING;
                    play_appropriate_music()
                for ev_t in pygame.event.get():
                    if ev_t.type == pygame.QUIT: running = False

            elif current_game_play_state == GAME_STATE_GAME_OVER_TIME:
                if game_over_lose_screen_image:
                    screen.blit(game_over_lose_screen_image, (0, 0))
                else:
                    display_centered_message("TEMPS ECOULE !", message_font, (200, 0, 0), -50)
                    display_centered_message("GAME OVER", message_font, (200, 0, 0), 50)
                final_score_text = f"Score Final: {score}"
                display_centered_message(final_score_text, final_score_font, (230, 230, 230), SCREEN_HEIGHT * 0.25)
                current_ticks_go = pygame.time.get_ticks()
                if current_ticks_go - game_over_time_display_start >= GAME_OVER_MESSAGE_DURATION:
                    game_launched_from_menu = False;
                    new_game_launched_flag_from_menu = False
                    current_game_play_state = GAME_STATE_MENU;
                    ui_screen_state_for_background = "menu";
                    play_appropriate_music()
                for ev_go in pygame.event.get():
                    if ev_go.type == pygame.QUIT: running = False

            elif current_game_play_state == GAME_STATE_GAME_OVER_WIN:
                if winner_screen_image: screen.blit(winner_screen_image, (0, 0))
                for ev_win in pygame.event.get():
                    if ev_win.type == pygame.QUIT: running = False

    elif not game_launched_from_menu and game_assets_loaded:
        game_assets_loaded = False;
        selected_avatar_imgs = None
        if "frames" in ball_state: ball_state["frames"] = []
    pygame.display.flip()
    clock.tick(60)
pygame.quit()