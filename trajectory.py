import pygame
import os
import math

def load_avatar(avatar_id):
    imgs={}; base="image/"
    try:
        p = "perso1" if avatar_id==2 else "pers2" if avatar_id==1 else "pers3" if avatar_id==3 else None
        if not p: print(f"Avatar ID {avatar_id} inconnu."); return None
        imgs["side"]=pygame.transform.scale(pygame.image.load(os.path.join(base,f"{p}side.png")).convert_alpha(),(200,200))
        imgs["lance"]=pygame.transform.scale(pygame.image.load(os.path.join(base,f"{p}lance.png")).convert_alpha(),(200,200))
    except pygame.error as e:print(f"Err load avatar {avatar_id}({p}):{e}");return None
    return imgs

def load_ball_frames(folder, count=15, scale=(90,100)):
    frames=[]
    if not os.path.isdir(folder):print(f"Dossier frames balle NI:{folder}");return frames
    try:
        base_name_parts = folder.split('/')[-1].replace('-ball', '').split('-')
        alt_path_prefix = base_name_parts[-1] if len(base_name_parts) > 0 else "ball"
        for i in range(1,count+1):
            possible_paths = [
                os.path.join(folder,f"frame{i}.png"),
                os.path.join(folder, f"{alt_path_prefix}_{i:02d}.png"),
                os.path.join(folder, f"{alt_path_prefix}{i}.png")
            ]
            path_found = None
            for p_path in possible_paths:
                if os.path.exists(p_path): path_found = p_path; break
            if not path_found:print(f"Frame {i} (et alts) manquante dans {folder}.");continue
            frames.append(pygame.transform.scale(pygame.image.load(path_found).convert_alpha(),scale))
    except pygame.error as e:print(f"Err load frames balle {folder}:{e}");return[]
    if not frames:print(f"Aucune frame chargée pour {folder}")
    return frames

def reset_ball_state(sw, sh):
    avatar_x_pos = 0; avatar_y_pos = sh - 220
    avatar_width = 200
    avatar_hand_offset_x = avatar_width * 0.8
    avatar_hand_offset_y = 50
    actual_start_x = avatar_x_pos + avatar_hand_offset_x
    actual_start_y = avatar_y_pos + avatar_hand_offset_y
    return {
        "frames":[], "frame_index":0, "frame_delay":3, "frame_counter":0,
        "start_x": actual_start_x, "start_y": actual_start_y,
        "x": actual_start_x, "y": actual_start_y,
        "t":0, "angle":math.radians(60), "velocity":7, "gravity":0.03,
        "shooting":False, "animation_done": False,
        "x_avatar":avatar_x_pos, "y_avatar": avatar_y_pos,
        "scored_this_throw":False, "vy_physics":0
    }

def update_ball(s, sw, sh, folder_unused):
    if not s["shooting"] or s.get("animation_done", False):
        if not s["shooting"]: s["x"]=s["start_x"]; s["y"]=s["start_y"]; s["frame_index"]=0
        return
    s["frame_counter"]+=1
    if s["frames"] and len(s["frames"])>0:
        if s["frame_counter"]>=s["frame_delay"]: s["frame_counter"]=0; s["frame_index"]=(s["frame_index"]+1)%len(s["frames"])
    else: s["frame_index"]=0
    s["t"] += 1
    s["x"]=s["start_x"]+s["velocity"]*s["t"]*math.cos(s["angle"])
    term_vy=s["velocity"]*s["t"]*math.sin(s["angle"]); term_g=s["gravity"]*s["t"]**2
    s["y"]=s["start_y"]-(term_vy-term_g)
    v0y=s["velocity"]*math.sin(s["angle"]); s["vy_physics"]=v0y-2*s["gravity"]*s["t"]
    bw=s["frames"][0].get_width() if s["frames"] else 0
    if s["x"]>sw+bw or s["y"]>sh+bw :
        if not (s["y"]<-sh*1.5 and s["vy_physics"]>0.05):
            cf=s["frames"]; ca=s["angle"]; cv=s["velocity"]
            nbs=reset_ball_state(sw,sh); s.clear(); s.update(nbs)
            s["frames"]=cf; s["angle"]=ca; s["velocity"]=cv

def draw_ball(surf, s, avatar_imgs):
    if avatar_imgs:
        img=avatar_imgs.get("lance") if s["shooting"] else avatar_imgs.get("side")
        if not img:img=avatar_imgs.get("lance",avatar_imgs.get("side"))
        if img:surf.blit(img,(s["x_avatar"],s["y_avatar"]))
    if s["frames"] and len(s["frames"])>0:
        idx=s["frame_index"]%len(s["frames"]); surf.blit(s["frames"][idx],(s["x"],s["y"]))

def launch_ball(s):
    if not s["shooting"]:
        s["shooting"]=True;s["t"]=0;s["x"]=s["start_x"];s["y"]=s["start_y"]
        s["animation_done"]=False;s["frame_index"]=0;s["scored_this_throw"]=False
        s["vy_physics"]=s["velocity"]*math.sin(s["angle"])

def adjust_ball_angle(s,d):
    if s["shooting"]:return
    deg=math.degrees(s["angle"])
    if d=="up" and deg<85:deg+=2
    elif d=="down" and deg>30:deg-=2
    s["angle"]=math.radians(deg)

def adjust_ball_velocity(s,d):
    if s["shooting"]:return
    min_vo=1;max_vo=15;inc=0.5
    if d=="right" and s["velocity"]<max_vo:s["velocity"]+=inc
    elif d=="left" and s["velocity"]>min_vo:s["velocity"]-=inc

def draw_trajectory_dots(surf,s,sw,sh,hoop_info=None):
    if s["shooting"]:return
    dot_col=(255,255,255); hoop_rect=None
    if hoop_info:hoop_rect=pygame.Rect(hoop_info["x"],hoop_info["y"],hoop_info["width"],hoop_info["height"])
    step_t=2; max_t_pred=120
    for td_sim in range(step_t,max_t_pred,step_t):
        xd=s["start_x"]+s["velocity"]*td_sim*math.cos(s["angle"])
        term_vy_p=s["velocity"]*td_sim*math.sin(s["angle"]);term_g_p=s["gravity"]*td_sim**2
        yd=s["start_y"]-(term_vy_p-term_g_p)
        v0y_p=s["velocity"]*math.sin(s["angle"]);vy_p_phys=v0y_p-2*s["gravity"]*td_sim
        if hoop_rect:
            dot_center=(int(xd),int(yd))
            if hoop_rect.collidepoint(dot_center) and vy_p_phys<0:
                for k_off_f in range(5):
                    td_ex=td_sim+k_off_f*step_t;
                    if td_ex>=max_t_pred:break
                    xd_ex=s["start_x"]+s["velocity"]*td_ex*math.cos(s["angle"])
                    term_vy_ex=s["velocity"]*td_ex*math.sin(s["angle"]);term_g_ex=s["gravity"]*td_ex**2
                    yd_ex=s["start_y"]-(term_vy_ex-term_g_ex)
                    if -sw*0.5 < xd_ex < sw*1.5 and -sh*2 < yd_ex < sh*1.5:
                         pygame.draw.circle(surf,dot_col,(int(xd_ex),int(yd_ex)),5)
                break
        draw_marg_yt=sh*2;draw_marg_xs=sw*0.75
        if xd<-draw_marg_xs or xd>sw+draw_marg_xs or yd>sh+100 or yd<-draw_marg_yt:
            if yd>sh+150 and vy_p_phys<0:break
            continue
        pygame.draw.circle(surf,dot_col,(int(xd),int(yd)),5)