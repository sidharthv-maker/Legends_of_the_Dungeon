fps = 60
w_width  = 1280
w_height = 720
title = "Legends of the Dungeon"
tile_size = 32

from sys import exit
from random import randint, choice
import pygame
import math
from data import REGULAR_ENEMIES, BOSSES, CHARACTER_TEMPLATES, PLAYER_SPEED_MAP, ENEMY_SPEED_MAP, CHAMPION_UPGRADE_COSTS
import json
import os

#Player
class Player:
    def __init__(self, x, y, template):
        def load(filename):
            img = pygame.image.load(f"assets/sprites/player/{template['sprite_folder']}/{filename}").convert_alpha()
            s = template.get("scale", 1.0)
            if s != 1.0:
                img = pygame.transform.scale(img, (int(img.get_width()*s), int(img.get_height()*s)))
            return img
        self.anims = {}
        for anim_key, filenames in template["sprites"].items():
            self.anims[anim_key] = [load(f) for f in filenames]
        self.speed = PLAYER_SPEED_MAP[template["speed"]]
        self.facing = "right"
        self.state = "idle"
        self.attacking = False
        self.attacks = template["attacks"]
        self.hp = template["max_hp"]
        self.max_hp = template["max_hp"]
        self.anim_frame = 0
        self.anim_timer = 0
        self.special_timers = [0, 0, 0, 0]
        self.basic_cd = 0
        self.invin = 0
        self.queued_proj = None
        self.proj_ready  = False
        self.gold = 0
        self.frame_duration = 0.15
        self.current_anim_key = "idle_right"
        self.player_rect = self.anims["idle_right"][0].get_rect(center=(x,y))

    def update(self, keys, dt):
        if not self.attacking:
            moving = False
            #X
            if keys[kset["right"]] or keys[kset["righta"]]:
                old_x = self.player_rect.x  
                self.player_rect.x += self.speed * dt
                cx, cy = int(self.player_rect.centerx), int(self.player_rect.centery)
                if not (0 <= cx < w_width and 0 <= cy < w_height and walk_mask.get_at((cx,cy))):
                    self.player_rect.x = old_x
                self.facing = "right"
                moving = True
            if keys[kset["left"]] or keys[kset["lefta"]]:
                old_x = self.player_rect.x
                self.player_rect.x -= self.speed * dt
                cx, cy = int(self.player_rect.centerx), int(self.player_rect.centery)
                if not (0 <= cx < w_width and 0 <= cy < w_height and walk_mask.get_at((cx, cy))):
                    self.player_rect.x = old_x
                self.facing = "left"
                moving = True
            #Y
            if keys[kset["up"]] or keys[kset["upa"]]:
                old_y = self.player_rect.y
                self.player_rect.y -= self.speed * dt
                cx, cy = int(self.player_rect.centerx), int(self.player_rect.centery)
                if not (0 <= cx < w_width and 0 <= cy < w_height and walk_mask.get_at((cx, cy))):
                    self.player_rect.y = old_y
                if not (keys[kset["left"]] or keys[kset["lefta"]] or keys[kset["right"]] or keys[kset["righta"]]):
                    self.facing = "back"
                moving = True
            if keys[kset["down"]] or keys[kset["downa"]]:
                old_y = self.player_rect.y
                self.player_rect.y += self.speed*dt
                cx, cy = int(self.player_rect.centerx), int(self.player_rect.centery)
                if not (0 <= cx < w_width and 0 <= cy < w_height and walk_mask.get_at((cx, cy))):
                    self.player_rect.y = old_y
                if not (keys[kset["left"]] or keys[kset["lefta"]] or keys[kset["right"]] or keys[kset["righta"]]):
                    self.facing = "front"
                moving = True
            self.state = "walk" if moving else "idle"
            anim_key = self.state + "_" + self.facing
            if anim_key not in self.anims:
                anim_key = "idle_" + self.facing
            if anim_key != self.current_anim_key:
                self.current_anim_key = anim_key
                self.anim_frame = 0
                self.anim_timer = 0
        self.anim_timer += dt
        if self.anim_timer >= self.frame_duration:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1)%len(self.anims[self.current_anim_key])
            if self.attacking and self.anim_frame == 0:
                if self.queued_proj is not None:
                    self.proj_ready = True
                self.attacking = False
        self.special_timers = [max(0, t - dt) for t in self.special_timers]
        self.basic_cd = max(0, self.basic_cd - dt)
        self.invin = max(0, self.invin - dt)

    def attack(self):
        if self.facing not in ("left", "right"):
            return False
        if self.attacking:
            return False
        if self.basic_cd > 0:
            return False
        self.basic_cd = 0
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "attack_" + self.facing
        return True

    def spattack(self, index):
        if self.facing not in ("left", "right"):
            return False
        if self.special_timers[index] > 0:
            return False
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "attack_" + self.facing
        self.special_timers[index] = 1.5*self.attacks[index+1]["cooldown"]
        return True

    def special(self, index):
        if self.facing not in ("left", "right"):
            return False
        if self.special_timers[index] > 0:
            return False
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "special_" + self.facing
        self.special_timers[index] = 1.5 * self.attacks[index+1]["cooldown"]
        return True

    def draw(self, screen):
        screen.blit(self.anims[self.current_anim_key][self.anim_frame], self.player_rect)
        #HP bar
        pygame.draw.rect(screen, (0, 80, 0),   (30, 0, 1200, 25))
        pygame.draw.rect(screen, (0, 200, 0),  (30, 0, int(1200*(self.hp/self.max_hp)), 25))
        font = pygame.font.SysFont(None, 36)
        screen.blit(font.render(f"Room {current_room+1}", True, (255,255,255)), (10, 30))
        screen.blit(font.render(f"Enemies: {len(enemies)}",True, (255,255,255)), (10, 60))
        #Cooldown boxes
        box_size = 50; box_gap = 10
        labels   = ["1","2","3","4"]
        total_w  = 4*box_size + 3*box_gap
        start_x  = (w_width - total_w) // 2
        box_y    = w_height - box_size - 10
        sf = pygame.font.SysFont(None, 24)
        for i in range(4):
            bx = start_x + i*(box_size+box_gap)
            col = (180,140,40) if self.special_timers[i] <= 0 else (60,60,60)
            pygame.draw.rect(screen,col,(bx, box_y, box_size, box_size))
            pygame.draw.rect(screen,(255,255,255),(bx, box_y, box_size, box_size),2)
            screen.blit(sf.render(labels[i], True,(255,255,255)), (bx+5, box_y+5))
            if self.special_timers[i] > 0:
                screen.blit(sf.render(f"{self.special_timers[i]:.1f}s",True,(200,200,200)),(bx+5,box_y+35))
        screen.blit(font.render(f"Gold: {self.gold}",True , (255,215,0)), (1150,10))


#Enemy
class Enemy:
    def __init__(self, x, y, data):
        def load(filename):
            return pygame.image.load(f"assets/sprites/enemies/{data['sprite_folder']}/{filename}").convert_alpha()
        if "sprites" in data:
            self.anims = {}
            for anim_key, filenames in data["sprites"].items():
                self.anims[anim_key] = [load(f) for f in filenames]
            self.facing = "right"
            self.current_anim_key = "idle_right"
            self.anim_frame = 0
            self.anim_timer = 0
            self.frame_duration = 0.15
        else:
            self.anims = None
        self.name = data["name"]
        self.max_hp = data["max_hp"]
        self.hp = data["max_hp"]
        self.dying = False
        self.dead = False
        self.speed = ENEMY_SPEED_MAP[data["speed"]]
        self.surf = pygame.Surface((40, 60))
        self.surf.fill((180, 60, 60))
        self.rect = self.surf.get_rect(center=(x, y))
        self.attacks = data["attacks"]
        self.attack_timer = 0
        self.attacking = False
        self.gold_awarded = False
        self.gold_value = data["reward_gold"]

    def update(self, player_rect, enemies, dt):
        if self.dying:
            if not self.gold_awarded:
                player.gold += self.gold_value
                self.gold_awarded = True
            if self.anims and "death" in self.anims:
                self.anim_timer += dt
                if self.anim_timer >= self.frame_duration:
                    self.anim_timer = 0
                    self.anim_frame += 1
                    if self.anim_frame >= len(self.anims["death"]):
                        self.dead = True
            else:
                self.dead = True
            return 0
        if self.hp <= 0:
            self.dying = True
            if self.anims and "death" in self.anims:
                self.current_anim_key = "death"
                self.anim_frame = 0
                self.anim_timer = 0
            return 0
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dis = math.sqrt(dx*dx + dy*dy)
        if dis != 0:
            dx /= dis; dy /= dis
        if dx > 0:
            self.facing = "right"
        else:
            self.facing = "left"
        if self.anims:
            if not self.attacking:
                anim_key = ("walk_" if dis > 80 else "idle_") + self.facing
                if anim_key != self.current_anim_key:
                    self.current_anim_key = anim_key
                    self.anim_frame = 0
                    self.anim_timer = 0
            self.anim_timer += dt
            if self.anim_timer >= self.frame_duration:
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame+1) % len(self.anims[self.current_anim_key])
                if self.attacking and self.anim_frame == 0:
                    self.attacking = False
        #movement + mask collision
        old_x = self.rect.x
        self.rect.x += dx * self.speed * dt
        cx, cy = int(self.rect.centerx), int(self.rect.centery)
        if not (0 <= cx < w_width and 0 <= cy < w_height and walk_mask.get_at((cx, cy))):
            self.rect.x = old_x
        old_y = self.rect.y
        self.rect.y += dy * self.speed * dt
        cx, cy = int(self.rect.centerx), int(self.rect.centery)
        if not (0 <= cx < w_width and 0 <= cy < w_height and walk_mask.get_at((cx, cy))):
            self.rect.y = old_y
        # separation
        for other in enemies:
            if other is not self and self.rect.colliderect(other.rect):
                dx1 = self.rect.centerx - other.rect.centerx
                dy1 = self.rect.centery - other.rect.centery
                d   = math.sqrt(dx1*dx1 + dy1*dy1)
                if d != 0:
                    self.rect.x += (dx1/d)*2
                    self.rect.y += (dy1/d)*2
        self.attack_timer -= dt
        if self.attack_timer <= 0 and dis < 80:
            atk = choice(self.attacks)
            damage = randint(atk["damage"][0], atk["damage"][1])
            self.attack_timer = 1.5 + atk["cooldown"]*0.5
            if self.anims:
                self.attacking = True
                self.current_anim_key = "attack_" + self.facing
                self.anim_frame = 0
                self.anim_timer = 0
            return damage
        return 0

    def draw(self, screen):
        if self.dead: return
        if self.anims:
            screen.blit(self.anims[self.current_anim_key][self.anim_frame], self.rect)
        else:
            screen.blit(self.surf, self.rect)
        bx, by = self.rect.x, self.rect.y - 12
        pygame.draw.rect(screen, (80,0,0),   (bx, by, 50, 6))
        pygame.draw.rect(screen, (200,0,0),  (bx, by, int(50*(self.hp/self.max_hp)), 6))


class Boss(Enemy):
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.speed = 100
        self.surf = pygame.Surface((60, 80))
        self.surf.fill((140, 0, 200))
        self.rect = self.surf.get_rect(center=(x, y))

class Projectile:
    def __init__(self, x, y, direction, damage, speed=520, img_path=None):
        if img_path:
            self.proj = pygame.image.load(img_path).convert_alpha()
        else:
            self.proj = pygame.Surface((20, 40))
            self.proj.fill((25, 12, 72))
        self.proj_rect = self.proj.get_rect(center=(x, y))
        self.direction = direction
        self.damage = damage
        self.speed = speed
        self.active = True
        
    def update(self, enemies, dt):
        if not self.active:
            return
        if self.direction == "right":
            self.proj_rect.x += int(self.speed * dt)
        else:
            self.proj_rect.x -= int(self.speed * dt)
        if self.proj_rect.right < 0 or self.proj_rect.left > w_width:
            self.active = False
            return
        for enemy in enemies:
            if self.proj_rect.colliderect(enemy.rect):
                cx, cy = self.proj_rect.centerx, self.proj_rect.centery
                for e in enemies:
                    if not e.dying:
                        dx = e.rect.centerx - cx
                        dy = e.rect.centery - cy
                        if math.sqrt(dx*dx + dy*dy) <= 100:
                            e.hp -= self.damage
                self.active = False
                break
        
    def draw(self,screen):
        screen.blit(self.proj, self.proj_rect)

kset = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "up": pygame.K_w,
    "down": pygame.K_s,
    "lefta": pygame.K_LEFT,
    "righta": pygame.K_RIGHT,
    "upa": pygame.K_UP,
    "downa": pygame.K_DOWN,
    "attack": pygame.K_j,
    "special1": pygame.K_1,
    "special2": pygame.K_2,
    "special3": pygame.K_3,
    "special4": pygame.K_4,
    "pause": pygame.K_ESCAPE,
}

def draw(screen, room_num):
    screen.blit(bg[room_num % 18], (0, 0))

nellipse = (60, 345, 1220, 320)
changes = {}

def get_ellipse(mapnum):
    return changes.get(mapnum,nellipse)

coords = [
    (270,450),(640,430),(1010,450),
    (200,525),(1060,525),
    (280,590),(640,580),(1000,590),
]

def generate_room(room_num):
    if (room_num+1) % 3 == 0:
        boss_data = BOSSES[(room_num//3) % len(BOSSES)]
        return [Boss(640, 250, boss_data)]
    if room_num < 3:   pool = REGULAR_ENEMIES[:4];  count = 3
    elif room_num < 6: pool = REGULAR_ENEMIES[4:8]; count = 4
    else:              pool = REGULAR_ENEMIES[8:];  count = 5
    result = []
    for i in range(count):
        data  = choice(pool)
        sx,sy = coords[i % len(coords)]
        result.append(Enemy(sx+randint(-30,30), sy+randint(-30,30), data))
    return result

pygame.init()
screen = pygame.display.set_mode((w_width,w_height))
clock = pygame.time.Clock()
pygame.display.set_caption(title)

bg = [
    pygame.transform.scale(pygame.image.load(f"assets/tilesets/map{i}.png").convert(), (w_width, w_height))
    for i in range(1, 19)
]

def build_walk_mask(map_number):
    mask_path = f"assets/tilesets/mask{map_number}.png"
    try:
        surf = pygame.image.load(mask_path).convert()
        surf = pygame.transform.scale(surf, (w_width, w_height))
        return pygame.mask.from_threshold(surf,(128,128,128),(128,128,128))
    except FileNotFoundError:
        s = pygame.Surface((w_width, w_height), pygame.SRCALPHA)
        s.fill((0,0,0,0))
        pygame.draw.ellipse(s, (255,255,255,255), get_ellipse(map_number))
        return pygame.mask.from_surface(s)

walk_masks = [build_walk_mask(i) for i in range(1, 19)]
walk_mask  = walk_masks[0]

# Shared UI
overlay = pygame.Surface((w_width, w_height), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 170))
enter_font = pygame.font.SysFont(None, 44)

#main menu
title_font = pygame.font.SysFont(None, 108)
sub_font   = pygame.font.SysFont(None, 38)
in_menu = True
while in_menu:
    clock.tick(fps)
    t = pygame.time.get_ticks() / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            in_menu = False
    screen.blit(bg[0],(0,0)); screen.blit(overlay, (0,0))
    pulse = (math.sin(1.8*t)+1)/2
    tr,tg,tb = int(200+55*pulse), int(150+55*pulse), int(20+20*pulse)
    ts = title_font.render("LEGENDS OF THE DUNGEON", True, (tr,tg,tb))
    screen.blit(ts, ts.get_rect(center=(w_width//2, w_height//2-90)))
    lw = ts.get_width(); lx = (w_width-lw)//2
    pygame.draw.line(screen,(tr,tg,tb),(lx,w_height//2-55),(lx+lw,w_height//2-55),2)
    ss = sub_font.render("A dungeon brawler", True, (160,160,175))
    screen.blit(ss, ss.get_rect(center=(w_width//2, w_height//2-20)))
    if int(t*2)%2==0:
        es = enter_font.render("PRESS  ENTER  TO  BEGIN", True, (220,200,110))
        screen.blit(es, es.get_rect(center=(w_width//2, w_height//2+70)))
    pygame.display.update()

# ── Game state ────────────────────────────────────────────────────────────────
current_room = 0
enemies = generate_room(current_room)
door_rect = pygame.Rect(w_width-tile_size,470,tile_size,80)
door_open = False
game_over = False
game_over_timer = 0
projectiles = []
proj_char = False

fpath = "save.txt"
pers_gold = 0

def load_val():
    if os.path.exists(fpath):
        with open(fpath, "r") as f:
            data = json.load(f)
        # Backwards compat: older saves won't have the upgrades key yet
        if "upgrades" not in data:
            data["upgrades"] = {"vitality": 0, "ferocity": 0, "fortune": 0}
        return data
    return {"pers_gold": 0, "upgrades": {"vitality": 0, "ferocity": 0, "fortune": 0}}

def write_val(data):
    with open(fpath, "w") as f:
        json.dump(data, f)

temp      = load_val()
pers_gold = temp["pers_gold"]
upgrades  = temp["upgrades"]

# Hub screen
hub_font  = pygame.font.SysFont(None, 64)
hub_sfont = pygame.font.SysFont(None, 36)
hub_idx   = 0          # 0 = PLAY, 1 = UPGRADES
hub_opts  = ["PLAY", "UPGRADES"]

# Shared fonts for the inner upgrades screen
upg_labels = ["Vitality(+15 HP/level)", "Ferocity(+10% dmg/level)", "Fortune(+15% gold/level)"]
upg_keys   = ["vitality", "ferocity", "fortune"]
star_font  = pygame.font.SysFont(None, 40)
cost_font  = pygame.font.SysFont(None, 30)

in_hub = True
while in_hub:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                hub_idx = (hub_idx - 1) % len(hub_opts)
            if event.key in (pygame.K_DOWN, pygame.K_s):
                hub_idx = (hub_idx + 1) % len(hub_opts)
            if event.key == pygame.K_RETURN:
                if hub_idx == 0:
                    in_hub = False  #proceed to character select

                else:
                    #Upgrades screen
                    in_upgrades = True
                    while in_upgrades:
                        clock.tick(fps)
                        for ev in pygame.event.get():
                            if ev.type == pygame.QUIT: pygame.quit(); exit()
                            if ev.type == pygame.KEYDOWN:
                                if ev.key in (pygame.K_UP, pygame.K_w):
                                    upg_idx = (upg_idx - 1) % 3
                                if ev.key in (pygame.K_DOWN, pygame.K_s):
                                    upg_idx = (upg_idx + 1) % 3
                                if ev.key in (pygame.K_j, pygame.K_SPACE, pygame.K_RETURN):
                                    #Attempt to buy next level of selected stat
                                    key = upg_keys[upg_idx]
                                    lvl = upgrades[key]
                                    if lvl < 5:
                                        cost = CHAMPION_UPGRADE_COSTS[key][lvl]
                                        if pers_gold >= cost:
                                            pers_gold     -= cost
                                            upgrades[key] += 1
                                            #Persist immediately so the purchase survives a crash
                                            write_val({"pers_gold": pers_gold, "upgrades": upgrades})
                                if ev.key == pygame.K_ESCAPE:
                                    in_upgrades = False  #back to hub

                        # Draw upgrades screen
                        screen.blit(bg[0], (0, 0))
                        screen.blit(overlay, (0, 0))
                        # Title
                        title_s = hub_font.render("UPGRADES", True, (220, 180, 50))
                        screen.blit(title_s, title_s.get_rect(center=(w_width // 2, 80)))
                        # Bank gold
                        bank_s = cost_font.render(f"Bank:  {pers_gold} gold", True, (255, 215, 0))
                        screen.blit(bank_s, bank_s.get_rect(center=(w_width // 2, 148)))
                        # Three stat rows
                        for row in range(3):
                            key     = upg_keys[row]
                            lvl     = upgrades[key]
                            ry      = 220 + row * 135
                            row_col = (255, 215, 0) if row == upg_idx else (200, 200, 200)
                            # Selection arrow
                            if row == upg_idx:
                                screen.blit(star_font.render(">", True, (255, 215, 0)), (120, ry + 6))
                            # Stat label
                            screen.blit(star_font.render(upg_labels[row], True, row_col), (160, ry))
                            # Stars: filled = purchased levels, empty = remaining slots
                            for s in range(5):
                                sc = (255, 215, 0) if s < lvl else (70, 70, 70)
                                pygame.draw.circle(screen, sc, (165 + s * 40, ry + 54), 15)
                                pygame.draw.circle(screen, (200, 200, 200), (165 + s * 40, ry + 54), 15, 2)
                            # Cost of next level or MAX badge
                            if lvl < 5:
                                cost     = CHAMPION_UPGRADE_COSTS[key][lvl]
                                cost_col = (255, 215, 0) if pers_gold >= cost else (180, 80, 80)
                                screen.blit(cost_font.render(f"Next: {cost}g", True, cost_col), (390, ry + 46))
                            else:
                                screen.blit(cost_font.render("MAX", True, (80, 220, 80)), (390, ry + 46))
                        # Controls hint at bottom
                        hint_s = cost_font.render("J / Space / Enter  =  Buy     ESC  =  Back", True, (130, 130, 130))
                        screen.blit(hint_s, hint_s.get_rect(center=(w_width // 2, w_height - 40)))
                        pygame.display.update()

    # Draw hub screen
    screen.blit(bg[0], (0, 0))
    screen.blit(overlay, (0, 0))
    title_s = hub_font.render("LEGENDS OF THE DUNGEON", True, (220, 180, 50))
    screen.blit(title_s, title_s.get_rect(center=(w_width // 2, 200)))
    for hi, opt in enumerate(hub_opts):
        col = (255, 215, 0) if hi == hub_idx else (180, 180, 180)
        ts  = hub_font.render(opt, True, col)
        screen.blit(ts, ts.get_rect(center=(w_width // 2, 340 + hi * 100)))
    bank_s = hub_sfont.render(f"Bank:  {pers_gold} gold", True, (255, 215, 0))
    screen.blit(bank_s, bank_s.get_rect(center=(w_width // 2, w_height - 50)))
    pygame.display.update()

#Character select
lst = ["Larry","Arthur","Akira","Zara","Drakon","Orion"]
i = 0
selected = lst[0]
selection = True
while selection:
    screen.blit(bg[1], (0,0)); screen.blit(overlay, (0,0))
    y = 100
    screen.blit(pygame.font.Font(None,32).render("Select your character",True,(169,169,169)),(520,0))
    for idx_n, name in enumerate(lst):
        col = (255,215,0) if idx_n==i else (169,169,169)
        screen.blit(pygame.font.Font(None,24).render(name,True,col),(520,y))
        y += 25
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: selected=lst[i]; selection=False; break
            if event.key == pygame.K_DOWN and i!=5: i+=1; selected=lst[i]
            if event.key == pygame.K_UP   and i!=0: i-=1; selected=lst[i]
    pygame.display.update()

proj_char = selected in ("Orion", "Zara")
player = Player(640, 450, CHARACTER_TEMPLATES[selected])

# ── Apply champion upgrades ────────────────────────────────────────────────────
# vitality: +15 max HP per level, refill HP to the new max
player.max_hp += upgrades["vitality"] * 15
player.hp      = player.max_hp
# ferocity: +10% damage multiplier per level — wire into damage rolls when you want
player.damage_mult = 1.0 + 0.10 * upgrades["ferocity"]
# fortune:  +15% gold multiplier per level — wire into enemy gold award when you want
player.gold_mult   = 1.0 + 0.15 * upgrades["fortune"]

#game loop
while True:
    dt = clock.tick(fps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()
        if event.type == pygame.KEYDOWN:
            #debugging
            if event.key == pygame.K_n:
                current_room += 1
                walk_mask = walk_masks[current_room % 18]
                enemies = generate_room(current_room)
                projectiles = []
                door_open = False
                player.player_rect.center = (640, 450)
                player.invin = 2.0

            #Game over restart
            if game_over and game_over_timer > 1.5:
                player.hp = player.max_hp
                player.player_rect.center = (640, 450)
                player.attacking = False
                player.anim_frame = 0
                player.anim_timer = 0
                player.current_anim_key = "idle_right"
                player.facing = "right"
                player.special_timers = [0,0,0,0]
                player.basic_cd = 0
                player.queued_proj = None
                player.proj_ready  = False
                player.invin   = 2.0
                player.gold = 0
                current_room = 0
                walk_mask = walk_masks[0]
                enemies = generate_room(current_room)
                projectiles = []
                door_open = False
                game_over = False
                game_over_timer= 0

            #Attacks
            if event.key == kset["attack"]:
                if proj_char:
                    if player.attack():
                        atk = player.attacks[0]
                        img = f"assets/sprites/player/orion/projectile_{player.facing}.png" if selected == "Orion" else None
                        player.queued_proj = {"facing": player.facing, "damage": randint(atk["damage"][0], atk["damage"][1]), "img_path": img}
                else:
                    if player.attack():
                        atk = player.attacks[0]
                        for enemy in enemies:
                            if player.player_rect.inflate(60,60).colliderect(enemy.rect):
                                enemy.hp -= int(randint(atk["damage"][0],atk["damage"][1]))

            if event.key == kset["special1"]:
                atk = player.attacks[1]
                if player.spattack(0):
                    for enemy in enemies:
                        if player.player_rect.inflate(80,80).colliderect(enemy.rect):
                            enemy.hp -= int(randint(atk["damage"][0],atk["damage"][1]))

            if event.key == kset["special2"]:
                atk = player.attacks[2]
                if player.spattack(1):
                    for enemy in enemies:
                        if player.player_rect.inflate(80,80).colliderect(enemy.rect):
                            enemy.hp -= int(randint(atk["damage"][0],atk["damage"][1]))

            if event.key == kset["special3"]:
                atk = player.attacks[3]
                if player.special(2):
                    for enemy in enemies:
                        if player.player_rect.inflate(80,80).colliderect(enemy.rect):
                            enemy.hp -= int(randint(atk["damage"][0],atk["damage"][1]))

            if event.key == kset["special4"]:
                atk = player.attacks[4]
                if player.special(3):
                    for enemy in enemies:
                        if player.player_rect.inflate(80,80).colliderect(enemy.rect):
                            enemy.hp -= int(randint(atk["damage"][0],atk["damage"][1]))

    keys = pygame.key.get_pressed()
    player.update(keys, dt)

    if player.proj_ready and player.queued_proj is not None:
        qp = player.queued_proj
        spawn_x = player.player_rect.right if qp["facing"] == "right" else player.player_rect.left
        spawn_y = player.player_rect.centery
        projectiles.append(Projectile(spawn_x, spawn_y, qp["facing"], qp["damage"], img_path=qp["img_path"]))
        player.queued_proj = None
        player.proj_ready  = False
    for enemy in enemies:
        dmg = enemy.update(player.player_rect, enemies, dt)
        if player.invin <= 0:
            player.hp -= dmg
    enemies = [e for e in enemies if not e.dead]

    for proj in projectiles:
        proj.update(enemies, dt)
    projectiles = [p for p in projectiles if p.active]

    #Player death
    if player.hp <= 0 and not game_over:
        game_over = True
        game_over_timer = 0
        pers_gold += player.gold
        write_val({"pers_gold": pers_gold, "upgrades": upgrades})  # save upgrades alongside gold
    if game_over:
        game_over_timer += dt

    #Draw
    draw(screen, current_room)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for proj in projectiles:
        proj.draw(screen)
    if game_over:
        f1 = pygame.font.SysFont(None, 80)
        f2 = pygame.font.SysFont(None, 36)
        screen.blit(f1.render("GAME OVER", True, (200,0,0)), (440,300))
        screen.blit(f2.render(f"Reached Room {current_room+1}", True,(255,255,255)),(520,380))
        if game_over_timer > 1.5:
            screen.blit(f2.render("Press any key to restart",True,(200,200,200)),(460,455))
        screen.blit(f1.render(f"Gold collected: {player.gold}", True, (255,215,0)), (460, 500))
        screen.blit(f2.render(f"Bank: {pers_gold} gold", True, (255,215,0)), (520, 415))
        

    #Door
    if len(enemies) == 0: door_open = True
    pygame.draw.rect(screen, (200,150,50) if door_open else (60,40,20), door_rect)
    if door_open:
        near_door = (player.player_rect.right >= w_width - tile_size - 5 and
                     door_rect.top < player.player_rect.centery < door_rect.bottom)
        if near_door:
            current_room += 1
            walk_mask   = walk_masks[current_room % 18]
            enemies     = generate_room(current_room)
            projectiles = []
            door_open   = False
            player.player_rect.center = (640, 450)
            player.invin = 2.0

    pygame.display.update()
