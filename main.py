from check_events import *
from level import *
from trajectory import *

ball_state = reset_ball_state(screen_width, screen_height)  # depuis level.py ou définis screen_width/height ici

running = True
difficulty_selector = 0
level = 0
score = 0

while running:
    running, game_launched, ball, avatar = menu_event()
    show_img()
    show_overlay()

    if game_launched:
        ball_state["frames"] = load_ball_frames(ball)
        difficulty_selector, level = basket_hoop(difficulty_selector, level, score)

        # MAJ de la balle
        update_ball(ball_state, screen_width, screen_height)
        draw_trajectory_dots(screen, ball_state, screen_width, screen_height)
        draw_ball(screen, ball_state)

        running = game_event(ball_state)

    pygame.display.flip()

pygame.quit()
