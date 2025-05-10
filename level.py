import pygame
import math

basket_img_original_raw = pygame.image.load("image/basket.png")
basket_img_scaled = None

difficulty = ["Easy", "Normal", "Intermediate", "Difficult"]
_basket_x = 900;
_basket_y = 175;
_basket_direction_x = 1;
_basket_direction_y = 1
_basket_state_machine = "right"

BASKET_WIDTH = 200;
BASKET_HEIGHT = 175;
MARGIN = 20
H_LIMIT_LEFT_ZONE = 0;
H_LIMIT_RIGHT_ZONE = 0
V_LIMIT_TOP_ZONE = 0;
V_LIMIT_BOTTOM_ZONE = 0
SQUARE_TL_R, SQUARE_TR_R, SQUARE_BR_R, SQUARE_BL_R = (0, 0), (0, 0), (0, 0), (0, 0)
T_TOP_L_R, T_TOP_R_R, T_STEM_TOP_R, T_STEM_BOTTOM_R = (0, 0), (0, 0), (0, 0), (0, 0)
TRI_PT_TOP_R, TRI_PT_LEFT_R, TRI_PT_RIGHT_R = (0, 0), (0, 0), (0, 0)
HEX_P1_R, HEX_P2_R, HEX_P3_R, HEX_P4_R, HEX_P5_R, HEX_P6_R = [(0, 0)] * 6


def init_level_assets(sw_param, sh_param):
    global basket_img_scaled, BASKET_WIDTH, BASKET_HEIGHT
    global H_LIMIT_LEFT_ZONE, H_LIMIT_RIGHT_ZONE, V_LIMIT_TOP_ZONE, V_LIMIT_BOTTOM_ZONE
    global SQUARE_TL_R, SQUARE_TR_R, SQUARE_BR_R, SQUARE_BL_R
    global T_TOP_L_R, T_TOP_R_R, T_STEM_TOP_R, T_STEM_BOTTOM_R
    global TRI_PT_TOP_R, TRI_PT_LEFT_R, TRI_PT_RIGHT_R
    global HEX_P1_R, HEX_P2_R, HEX_P3_R, HEX_P4_R, HEX_P5_R, HEX_P6_R

    basket_img_original_converted = basket_img_original_raw.convert_alpha()
    basket_img_scaled = pygame.transform.smoothscale(basket_img_original_converted, (200, 175))
    BASKET_WIDTH = basket_img_scaled.get_width();
    BASKET_HEIGHT = basket_img_scaled.get_height()

    H_LIMIT_LEFT_ZONE = sw_param / 2 + MARGIN
    H_LIMIT_RIGHT_ZONE = sw_param - BASKET_WIDTH - MARGIN
    V_LIMIT_TOP_ZONE = MARGIN + 50
    V_LIMIT_BOTTOM_ZONE = sh_param - BASKET_HEIGHT - MARGIN - 50

    square_size = 150
    SQUARE_TL_R = (H_LIMIT_LEFT_ZONE + 50, V_LIMIT_TOP_ZONE + 50)
    SQUARE_TR_R = (SQUARE_TL_R[0] + square_size, SQUARE_TL_R[1])
    SQUARE_BR_R = (SQUARE_TR_R[0], SQUARE_TR_R[1] + square_size)
    SQUARE_BL_R = (SQUARE_TL_R[0], SQUARE_BR_R[1])

    t_bar_width = 200;
    t_stem_height = 150
    T_TOP_L_R = ((H_LIMIT_LEFT_ZONE + H_LIMIT_RIGHT_ZONE - t_bar_width) // 2, V_LIMIT_TOP_ZONE + 50)
    T_TOP_R_R = (T_TOP_L_R[0] + t_bar_width, T_TOP_L_R[1])
    T_STEM_TOP_R = (T_TOP_L_R[0] + t_bar_width // 2, T_TOP_L_R[1])
    T_STEM_BOTTOM_R = (T_STEM_TOP_R[0], T_STEM_TOP_R[1] + t_stem_height)

    tri_base_width = 200;
    tri_height = 150
    TRI_PT_TOP_R = ((H_LIMIT_LEFT_ZONE + H_LIMIT_RIGHT_ZONE) // 2, V_LIMIT_TOP_ZONE + 30)
    TRI_PT_LEFT_R = (TRI_PT_TOP_R[0] - tri_base_width // 2, TRI_PT_TOP_R[1] + tri_height)
    TRI_PT_RIGHT_R = (TRI_PT_TOP_R[0] + tri_base_width // 2, TRI_PT_TOP_R[1] + tri_height)

    hex_radius = 80
    hex_center_x_zone = (H_LIMIT_LEFT_ZONE + H_LIMIT_RIGHT_ZONE) // 2
    hex_center_y_zone = (V_LIMIT_TOP_ZONE + V_LIMIT_BOTTOM_ZONE) // 2
    HEX_P1_R = (hex_center_x_zone - hex_radius // 2, hex_center_y_zone - int(hex_radius * math.sqrt(3) / 2))
    HEX_P2_R = (hex_center_x_zone + hex_radius // 2, hex_center_y_zone - int(hex_radius * math.sqrt(3) / 2))
    HEX_P3_R = (hex_center_x_zone + hex_radius, hex_center_y_zone)
    HEX_P4_R = (hex_center_x_zone + hex_radius // 2, hex_center_y_zone + int(hex_radius * math.sqrt(3) / 2))
    HEX_P5_R = (hex_center_x_zone - hex_radius // 2, hex_center_y_zone + int(hex_radius * math.sqrt(3) / 2))
    HEX_P6_R = (hex_center_x_zone - hex_radius, hex_center_y_zone)


def get_basket_rect():
    if basket_img_scaled: return basket_img_scaled.get_rect()
    return pygame.Rect(0, 0, 0, 0)


def reset_basket_position_for_level(diff_sel_idx, lvl_val, SW, SH):
    global _basket_x, _basket_y, _basket_direction_x, _basket_direction_y, _basket_state_machine
    diff_name = difficulty[diff_sel_idx]
    _basket_x = H_LIMIT_LEFT_ZONE;
    _basket_y = V_LIMIT_TOP_ZONE + (V_LIMIT_BOTTOM_ZONE - V_LIMIT_TOP_ZONE) // 2
    _basket_direction_x = 1;
    _basket_direction_y = 1
    if diff_name == "Easy":
        _basket_x = (H_LIMIT_LEFT_ZONE + H_LIMIT_RIGHT_ZONE) // 2; _basket_y = V_LIMIT_TOP_ZONE + 50
    elif diff_name == "Normal" or diff_name == "Intermediate":
        if lvl_val == 0:
            _basket_x = H_LIMIT_LEFT_ZONE; _basket_state_machine = "right"
        elif lvl_val == 1:
            _basket_y = V_LIMIT_TOP_ZONE; _basket_state_machine = "down"
        elif lvl_val == 2:
            _basket_x = SQUARE_TL_R[0]; _basket_y = SQUARE_TL_R[1]; _basket_state_machine = "square_R_to_TR"
    elif diff_name == "Difficult":
        if lvl_val == 0:
            _basket_x, _basket_y = T_TOP_L_R; _basket_state_machine = "t_R_bar_right"
        elif lvl_val == 1:
            _basket_x = H_LIMIT_LEFT_ZONE; _basket_y = V_LIMIT_TOP_ZONE; _basket_state_machine = "diag_R_down_right"
        elif lvl_val == 2:
            _basket_x, _basket_y = TRI_PT_TOP_R; _basket_state_machine = "tri_R_to_left_bottom"
        elif lvl_val == 3:
            _basket_x, _basket_y = SQUARE_TL_R; _basket_state_machine = "square_R_to_TR"
        elif lvl_val == 4:
            _basket_x, _basket_y = HEX_P1_R; _basket_state_machine = "hex_R_to_p2"


def move_towards_target(cur, tar, spd):
    dx = tar[0] - cur[0];
    dy = tar[1] - cur[1];
    dist = math.sqrt(dx ** 2 + dy ** 2)
    if dist < spd * 1.1: return tar, True
    return (cur[0] + (dx / dist) * spd, cur[1] + (dy / dist) * spd), False


def basket_hoop(screen_surface, cur_diff_sel, cur_lvl, SW, SH):
    global _basket_x, _basket_y, _basket_direction_x, _basket_direction_y, _basket_state_machine
    if not basket_img_scaled: return _basket_x, _basket_y
    diff_name = difficulty[cur_diff_sel];
    lvl = cur_lvl;
    speed = 0
    if diff_name == "Easy":
        speed = 0
    elif diff_name == "Normal":
        speed = 1.8
    elif diff_name == "Intermediate":
        speed = 3.0
    elif diff_name == "Difficult":
        speed = 4.0

    h_lim_l, h_lim_r = H_LIMIT_LEFT_ZONE, H_LIMIT_RIGHT_ZONE
    v_lim_t, v_lim_b = V_LIMIT_TOP_ZONE, V_LIMIT_BOTTOM_ZONE

    if diff_name == "Easy":
        pass
    elif diff_name == "Normal" or diff_name == "Intermediate":
        if lvl == 0:
            _basket_x += _basket_direction_x * speed
            if (_basket_direction_x == 1 and _basket_x >= h_lim_r) or (
                    _basket_direction_x == -1 and _basket_x <= h_lim_l): _basket_direction_x *= -1;_basket_x = max(
                h_lim_l, min(_basket_x, h_lim_r))
        elif lvl == 1:
            _basket_y += _basket_direction_y * speed
            if (_basket_direction_y == 1 and _basket_y >= v_lim_b) or (
                    _basket_direction_y == -1 and _basket_y <= v_lim_t): _basket_direction_y *= -1;_basket_y = max(
                v_lim_t, min(_basket_y, v_lim_b))
        elif lvl == 2:
            target_pos = (_basket_x, _basket_y);
            next_s_state = _basket_state_machine
            if _basket_state_machine == "square_R_to_TR":
                target_pos = SQUARE_TR_R; next_s_state = "square_R_to_BR"
            elif _basket_state_machine == "square_R_to_BR":
                target_pos = SQUARE_BR_R; next_s_state = "square_R_to_BL"
            elif _basket_state_machine == "square_R_to_BL":
                target_pos = SQUARE_BL_R; next_s_state = "square_R_to_TL"
            elif _basket_state_machine == "square_R_to_TL":
                target_pos = SQUARE_TL_R; next_s_state = "square_R_to_TR"
            new_pos, reached = move_towards_target((_basket_x, _basket_y), target_pos, speed)
            _basket_x, _basket_y = new_pos
            if reached: _basket_state_machine = next_s_state
    elif diff_name == "Difficult":
        cur_p = (_basket_x, _basket_y);
        tar_p = cur_p;
        next_s = _basket_state_machine
        if lvl == 0:
            if _basket_state_machine == "t_R_bar_right":
                tar_p = T_TOP_R_R;next_s = "t_R_bar_left_then_stem"
            elif _basket_state_machine == "t_R_bar_left_then_stem":
                tar_p = T_TOP_L_R;next_s = "t_R_stem_down"
            elif _basket_state_machine == "t_R_stem_down":
                tar_p = T_STEM_BOTTOM_R;next_s = "t_R_stem_up_then_bar"
            elif _basket_state_machine == "t_R_stem_up_then_bar":
                tar_p = T_STEM_TOP_R;next_s = "t_R_bar_right"
        elif lvl == 1:
            tdr = (H_LIMIT_RIGHT_ZONE, V_LIMIT_BOTTOM_ZONE);
            tul = (H_LIMIT_LEFT_ZONE, V_LIMIT_TOP_ZONE)
            if _basket_state_machine == "diag_R_down_right":
                tar_p = tdr;next_s = "diag_R_up_left"
            elif _basket_state_machine == "diag_R_up_left":
                tar_p = tul;next_s = "diag_R_down_right"
        elif lvl == 2:
            if _basket_state_machine == "tri_R_to_left_bottom":
                tar_p = TRI_PT_LEFT_R;next_s = "tri_R_to_right_bottom"
            elif _basket_state_machine == "tri_R_to_right_bottom":
                tar_p = TRI_PT_RIGHT_R;next_s = "tri_R_to_top"
            elif _basket_state_machine == "tri_R_to_top":
                tar_p = TRI_PT_TOP_R;next_s = "tri_R_to_left_bottom"
        elif lvl == 3:
            if _basket_state_machine == "square_R_to_TR":
                tar_p = SQUARE_TR_R;next_s = "square_R_to_BR"
            elif _basket_state_machine == "square_R_to_BR":
                tar_p = SQUARE_BR_R;next_s = "square_R_to_BL"
            elif _basket_state_machine == "square_R_to_BL":
                tar_p = SQUARE_BL_R;next_s = "square_R_to_TL"
            elif _basket_state_machine == "square_R_to_TL":
                tar_p = SQUARE_TL_R;next_s = "square_R_to_TR"
        elif lvl == 4:
            if _basket_state_machine == "hex_R_to_p2":
                tar_p = HEX_P2_R;next_s = "hex_R_to_p3"
            elif _basket_state_machine == "hex_R_to_p3":
                tar_p = HEX_P3_R;next_s = "hex_R_to_p4"
            elif _basket_state_machine == "hex_R_to_p4":
                tar_p = HEX_P4_R;next_s = "hex_R_to_p5"
            elif _basket_state_machine == "hex_R_to_p5":
                tar_p = HEX_P5_R;next_s = "hex_R_to_p6"
            elif _basket_state_machine == "hex_R_to_p6":
                tar_p = HEX_P6_R;next_s = "hex_R_to_p1"
            elif _basket_state_machine == "hex_R_to_p1":
                tar_p = HEX_P1_R;next_s = "hex_R_to_p2"
        new_p, reached = move_towards_target(cur_p, tar_p, speed);
        _basket_x, _basket_y = new_p
        if reached: _basket_state_machine = next_s

    _basket_x = max(H_LIMIT_LEFT_ZONE, min(_basket_x, H_LIMIT_RIGHT_ZONE))
    _basket_y = max(V_LIMIT_TOP_ZONE, min(_basket_y, V_LIMIT_BOTTOM_ZONE))
    screen_surface.blit(basket_img_scaled, (_basket_x, _basket_y))
    return _basket_x, _basket_y