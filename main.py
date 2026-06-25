fps = 60
w_width  = 1280
w_height = 720
title    = "Legends of the Dungeon"
tile_size = 32

from sys import exit
from random import randint, choice
import pygame
import math
from data import REGULAR_ENEMIES, BOSSES, CHARACTER_TEMPLATES, PLAYER_SPEED_MAP, ENEMY_SPEED_MAP


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
        self.invin = 0
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
                self.attacking = False
        self.special_timers = [max(0, t - dt) for t in self.special_timers]
        self.invin = max(0, self.invin - dt)

    def attack(self):
        if self.facing not in ("left", "right"):
            return
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "attack_" + self.facing

    def spattack(self, index):
        if self.facing not in ("left", "right"):
            return False
        if self.special_timers[index] > 0:
            return False
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "attack_" + self.facing
        self.special_timers[index] = 1.5*self.attacks[index]["cooldown"]
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
        self.special_timers[index] = 1.5 * self.attacks[index]["cooldown"]
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

    def update(self, player_rect, enemies, dt):
        if self.dying:
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

#Character select
lst = ["Larry","Arthur","Akira","Zara","Drakon","Orion"]
i = 0; selected = lst[0]; selection = True
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

player = Player(640, 450, CHARACTER_TEMPLATES[selected])

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
                enemies   = generate_room(current_room)
                door_open = False
                player.player_rect.center = (640, 450)
                player.invin = 2.0

            #Game over restart
            if game_over and game_over_timer > 1.5:
                player.hp     = player.max_hp
                player.player_rect.center = (640, 450)
                player.attacking = False
                player.anim_frame = 0; player.anim_timer = 0
                player.current_anim_key = "idle_right"
                player.facing  = "right"
                player.special_timers = [0,0,0,0]
                player.invin   = 2.0
                current_room   = 0
                walk_mask      = walk_masks[0]
                enemies        = generate_room(current_room)
                door_open      = False
                game_over      = False
                game_over_timer= 0

            #Attacks
            if event.key == kset["attack"]:
                player.attack()
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
    for enemy in enemies:
        dmg = enemy.update(player.player_rect, enemies, dt)
        if player.invin <= 0:
            player.hp -= dmg
    enemies = [e for e in enemies if not e.dead]

    #Player death
    if player.hp <= 0 and not game_over:
        game_over       = True
        game_over_timer = 0
    if game_over:
        game_over_timer += dt

    #Draw
    draw(screen, current_room)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    if game_over:
        f1 = pygame.font.SysFont(None, 80)
        f2 = pygame.font.SysFont(None, 36)
        screen.blit(f1.render("GAME OVER", True, (200,0,0)), (440,300))
        screen.blit(f2.render(f"Reached Room {current_room+1}", True,(255,255,255)),(520,380))
        if game_over_timer > 1.5:
            screen.blit(f2.render("Press any key to restart",True,(200,200,200)),(460,455))

    #Door
    if len(enemies) == 0: door_open = True
    pygame.draw.rect(screen, (200,150,50) if door_open else (60,40,20), door_rect)
    if door_open:
        near_door = (player.player_rect.right >= w_width - tile_size - 5 and
                     door_rect.top < player.player_rect.centery < door_rect.bottom)
        if near_door:
            current_room += 1
            walk_mask = walk_masks[current_room % 18]
            enemies   = generate_room(current_room)
            door_open = False
            player.player_rect.center = (640, 450)
            player.invin = 2.0

    pygame.display.update()
