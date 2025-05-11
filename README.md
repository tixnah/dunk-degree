# Dunk & Degree

## Suject

* Transverse Project :

Teams of students collaborate to provide a technical solution to a validated need by leveraging all of their learning outcomes at their level of study.


* Problematic :

**How to optimize the precision and speed of shots to maximize the number of successful baskets in a limited time ?**




* Description:

Simulator of a basketball game, including variable (time, speed), trajectory (curve), feedback (advice to help), graphic report and programming, the goal being to score a maximum of points in a limited time. 


___________

## Game

**Gameplay :**

- Time decreasing on the player's screen.
- Different levels (Easy, Normal, Difficult)

**Level :**

- Easy : the basket doesn’t move
    - level 1
    - level 2
    - level 3
- Normal : the basket move slowly  (left to right / up to done / every direction)
    - level 4
    - level 5
    - level 6
- Intermediate : the basket move at an average speed (left to right / up to down / left, right, up and down / diagonals)
    - level 7
    - level 8
    - level 9
- Difficult : the basket move faster at every game (left to right / up to down / left, right, up and down / diagonals)
    - level 10
    - level 11
    - level 12
    - level 13
    - level 14

**How to play :**

  Use the arrow keys of your keyboard to adjust the trajectory you want, then click on the space bar to shoot when you are ready.
  Once the ball goes through the basket, your score increases of 1.
  You have 30 seconds on each level to score the maximum of points you can.

___________

## Coding part

**The modules used :**

- pygame for the graphical display
- time for the chronometer
- math for the levels and the trjectory
- os for the interactions between the user and the program


**The functions created :**

In the "level.py" file : 

- init_level_assets(sw_param, sh_param) : 
    Initializes the level assets and settings.
    Resizes and converts the basket image.
    Updates the bazsket's overall dimensions.
    Calculates the bounds of the bazsket's movement area.
    Calculates the coordinates of path points for complex movements.
- get_basket_rect() :
    Flips the basket rectangle
    Returns: pygame.Rect: The basket image rectangle, or an empty rectangle if not loaded.
- reset_basket_position_for_level(diff_sel_idx, lvl_val, SW_UNUSED, SH_UNUSED) :
    Resets the starting position and movement state of the basket based on the selected difficulty and level.
- move_towards_target(cur, tar, spd) :
    Computes the new position for a movement from point 'cur' to point 'tar' at speed 'spd'.
- basket_hoop(screen_surface, cur_diff_sel, cur_lvl, SW_UNUSED, SH_UNUSED) :
    Manages the movement and display of the basket. Movement logic depends on the current difficulty and level.



In the "trajectory.py" file : 

- load_avatar(avatar_id) : 
    Loads images of a specific avatar.
- load_ball_frames(folder, count=15, scale=(90, 100)) : 
    Loads a sequence of images (frames) for the ball animation from a specified folder. Tries several naming conventions for the frame files. The frames are resized.
- reset_ball_state(sw, sh) :
    Resets the ball's state to its default values ​​(starting position, current shot, etc.). The ball's starting position is calculated based on the avatar's position.
- update_ball(s, sw, sh, folder_unused) :
    Updates the ball's state every game tick. 
    Manages the ball's animation and physical trajectory if it's being kicked. 
    Resets the ball if it goes off-screen.
- draw_ball(surf, s, avatar_imgs) :
    Draw the avatar and the ball on the given surface.
- launch_ball(s) :
    Initializes the ball shooting process. Sets the "shooting" state to True and resets the shooting physics variables.
- adjust_ball_angle(s, d) :
    Adjusts the angle at which the ball is shot (if the ball is not being shot).
- adjust_ball_velocity(s, d) :
    Adjusts the ball's shooting power.
- draw_trajectory_dots(surf, s, sw, sh, hoop_info=None) :
    Draws a preview of the ball's trajectory as points.



In the "sound_manager.py" file :

- init_mixer() :
    Initializes the 'pygame.mixer' module if it is not already initialized.
- play_music(key, loops=-1, volume=0.5, fade_ms=1000) : 
    Plays a song identified by its key. Manages crossfading if another song is already playing.
- stop_music() :
    Stops the currently playing music and unloads it.
- fadeout_music(time_ms) :
    Fades out the currently playing music. The music will stop after the fade.
- set_volume(volume) :
    Sets the volume of the music.
- is_playing(key=None) :
    Checks if a song is playing. If a key is provided, checks if THIS specific song is playing.



In the "main.py" file :

- get_global_level_number(cur_diff_sel, cur_lvl_val) :
    Calculates the overall level number based on the difficulty and the current level in that difficulty. Allows for a continuous "Level X" display across difficulties.
- load_level_transition_image(gl_lvl_num) :
    Loads (or retrieves from cache) the transition image for a given global level number.
- play_appropriate_music() :
    Plays the appropriate music based on the current game state and difficulty. Also manages global music on/off.
- start_new_level_setup() :
    Initializes the parameters for a new level. Changes to the level transition state.
- advance_to_next_challenge() :
    Goes to the next level or difficulty if the current level is completed. If all levels on all difficulties are completed, goes to the victory screen.
- display_centered_message(txt, fnt, col=(255, 255, 255), y_off=0, aa=True) :
    Displays a centered text message on the screen.
        
