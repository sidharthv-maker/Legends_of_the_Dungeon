fps = 60
w_width= 1280
w_height = 720
title = "Legends of the Dungeon"
tile_size = 32

from sys import exit
from random import randint, choice
import pygame
import math
from data import REGULAR_ENEMIES,BOSSES,CHARACTER_TEMPLATES

class Player:
    def __init__(self, x, y, name, template):
        def load(filename):
            return pygame.image.load(f"assets/sprites/player/{name}/{filename}").convert_alpha()
            # return pygame.transform.scale(img,(3*img.get_width(), 3*img.get_height()))
        self.anims = {
            "idle_left": [load("akira_idle_left_f1.png"),  load("akira_idle_left_f2.png")],
            "idle_right": [load("akira_idle_right_f1.png"), load("akira_idle_right_f2.png")],
            "idle_front": [load("akira_main_front.png")],
            "idle_back": [load("akira_main_back.png")],
            "walk_left": [load("akira_walk_left_f1.png"),  load("akira_walk_left_f2.png"),  load("akira_walk_left_f3.png")],
            "walk_right": [load("akira_walk_right_f1.png"), load("akira_walk_right_f2.png"), load("akira_walk_right_f3.png")],
            "attack_right": [load("akira_basic_left_f1.png"),  load("akira_basic_left_f2.png")],
            "attack_left": [load("akira_basic_right_f1.png"), load("akira_basic_right_f2.png")],
            "special_right": [load("akira_special_left_f1.png"), load("akira_special_left_f2.png"), load("akira_special_left_f3.png")],
            "special_left": [load("akira_special_right_f1.png"), load("akira_special_right_f2.png"), load("akira_special_right_f3.png")]
        }
        self.speed = 300
        self.facing = "right"
        self.state = "idle"
        self.attacking = False
        self.attacks = template["attacks"]
        self.hp = template["max_hp"]
        self.max_hp = template["max_hp"]
        self.anim_frame = 0
        self.anim_timer = 0
        self.special_timers = [0, 0, 0, 0]
        self.frame_duration = 0.15
        self.current_anim_key = "idle_right"
        self.player_rect = self.anims["idle_right"][0].get_rect(center=(x,y))

    def update(self, keys, wall_rects, dt):
        if not self.attacking:
            moving = False
            #move right
            if keys[kset["right"]] or keys[kset["righta"]]:
                self.player_rect.x += self.speed*dt
                for wall in wall_rects:
                    if self.player_rect.colliderect(wall):
                        self.player_rect.right = wall.left
                self.facing = "right"
                moving = True
            #move left
            if keys[kset["left"]] or keys[kset["lefta"]]:
                self.player_rect.x -= self.speed*dt
                for wall in wall_rects:
                    if self.player_rect.colliderect(wall):
                        self.player_rect.left = wall.right
                self.facing = "left"
                moving = True
            #move up
            if keys[kset["up"]] or keys[kset["upa"]]:
                self.player_rect.y -= self.speed*dt
                for wall in wall_rects:
                    if self.player_rect.colliderect(wall):
                        self.player_rect.top = wall.bottom
                if not (keys[kset["left"]] or keys[kset["lefta"]] or keys[kset["right"]] or keys[kset["righta"]]):
                    self.facing = "back"
                moving = True
            #move down
            if keys[kset["down"]] or keys[kset["downa"]]:
                self.player_rect.y += self.speed*dt
                for wall in wall_rects:
                    if self.player_rect.colliderect(wall):
                        self.player_rect.bottom = wall.top
                if not (keys[kset["left"]] or keys[kset["lefta"]] or keys[kset["right"]] or keys[kset["righta"]]):
                    self.facing = "front"
                moving = True
            #update state
            self.state = "walk" if moving else "idle"
            #resolve anim key (walk_front/back don't exist, fall back to idle)
            anim_key = self.state + "_" + self.facing
            if anim_key not in self.anims:
                anim_key = "idle_" + self.facing
            #reset frame if animation changed
            if anim_key != self.current_anim_key:
                self.current_anim_key = anim_key
                self.anim_frame = 0
                self.anim_timer = 0
            #advance frame
        self.anim_timer += dt
        if self.anim_timer >= self.frame_duration:
            self.anim_timer = 0
            self.anim_frame = (self.anim_frame + 1) % len(self.anims[self.current_anim_key])
            if self.attacking and self.anim_frame == 0:
                self.attacking = False
        self.special_timers = [max(0, t - dt) for t in self.special_timers]
    
    def attack(self):
        if self.facing not in ("left", "right"):
            return
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "attack_" + self.facing
    
    def spattack(self,index):
        if self.facing not in ("left", "right"):
            return False
        if self.special_timers[index] > 0:
            return False  #still on cooldown
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "attack_" + self.facing
        self.special_timers[index] = self.attacks[index]["cooldown"]*1.5
        return True
    
    def special(self, index):
        if self.facing not in ("left", "right"):
            return False
        if self.special_timers[index] > 0:
            return False  #still on cooldown
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "special_" + self.facing
        self.special_timers[index] = self.attacks[index]["cooldown"]*1.5
        return True
    
    def draw(self, screen):
        current_anim = self.anims[self.current_anim_key]
        screen.blit(current_anim[self.anim_frame],self.player_rect)
        bar_width  = 1200
        bar_height = 25
        bar_x = 30
        bar_y = 0
        pygame.draw.rect(screen, (0, 80, 0),(bar_x, bar_y, bar_width, bar_height))
        current_width = int(bar_width*(self.hp/self.max_hp))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, current_width, bar_height))

class Enemy:
    def __init__(self, x, y, data):
        self.name = data["name"]
        self.max_hp  = data["max_hp"]
        self.hp = data["max_hp"]
        self.speed = 150
        self.surf = pygame.Surface((40, 60))
        self.surf.fill((180, 60, 60))
        self.rect = self.surf.get_rect(center=(x, y))
        self.attacks = data["attacks"]
        self.attack_timer = 0

    def update(self, player_rect, enemies, dt):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dis = math.sqrt(dx*dx + dy*dy)
        if dis != 0:
            dx /= dis
            dy /= dis
        self.rect.x += dx*self.speed*dt
        for wall in wall_rects:
            if self.rect.colliderect(wall):
                if dx > 0: self.rect.right = wall.left
                else: self.rect.left = wall.right
        self.rect.y += dy*self.speed*dt
        for wall in wall_rects:
            if self.rect.colliderect(wall):
                if dy > 0: self.rect.bottom = wall.top
                else: self.rect.top = wall.bottom
        # separate from other enemies
        for other in enemies:
            if other is not self and self.rect.colliderect(other.rect):
                dx1 = self.rect.centerx - other.rect.centerx
                dy1 = self.rect.centery - other.rect.centery
                dis1 = math.sqrt(dx1*dx1 + dy1*dy1)
                if dis1 != 0:
                    self.rect.x += (dx1/dis1)*2
                    self.rect.y += (dy1/dis1)*2
        
        self.attack_timer -= dt
        if self.attack_timer <= 0 and dis<80:
            atk = choice(self.attacks)
            damage = randint(atk["damage"][0], atk["damage"][1])
            self.attack_timer = 1.5 + atk["cooldown"]*0.5
            return damage
        return 0

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        bar_width  = 50
        bar_height = 6
        bar_x = self.rect.x
        bar_y = self.rect.y - 12
        pygame.draw.rect(screen, (80, 0, 0),(bar_x, bar_y, bar_width, bar_height))
        current_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(screen, (200, 0, 0),(bar_x, bar_y, current_width, bar_height))

class Boss(Enemy):
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.speed = 100
        self.surf  = pygame.Surface((60, 80))
        self.surf.fill((140, 0, 200))
        self.rect  = self.surf.get_rect(center=(x, y))
    

kset = {
"left"  : pygame.K_a,
"right" : pygame.K_d,
"up"    : pygame.K_w,
"down"  : pygame.K_s,
"lefta"  : pygame.K_LEFT,
"righta" : pygame.K_RIGHT,
"upa"    : pygame.K_UP,
"downa"  : pygame.K_DOWN,
"attack"     : pygame.K_j,
"special1"  : pygame.K_1,
"special2"  : pygame.K_2,
"special3"  : pygame.K_3,
"special4"  : pygame.K_4,
"pause"      : pygame.K_ESCAPE,
}

cols = 40
rows = 23

map_width  = cols*tile_size
map_height = rows*tile_size
wall_rects = []

for col in range(cols):
    for row in range(rows):
        if col == 0 or col == cols-1 or row == 0 or row == rows-1:
            wall_rects.append(pygame.Rect(col*tile_size, row*tile_size,tile_size,tile_size))

def draw(screen, room_num):
    if room_num%3 == 0:
        screen.blit(bg[0], (0, 0))
    elif room_num%3 == 1:
        screen.blit(bg[1], (0, 0))
    else:
        screen.blit(bg[2], (0, 0))

# spawn points spread around the room, away from center and walls
coords = [(250, 180), (640, 150), (1000, 180),(200, 360),(1050, 360),(250, 530), (640, 560), (1000, 530),]

def generate_room(room_num):
    # every 3rd room is a boss (room 2, 5, 8 ... index-wise)
    if (room_num + 1) % 3 == 0:
        boss_data = BOSSES[(room_num // 3) % len(BOSSES)]
        return [Boss(640, 250, boss_data)]
    # pick enemy tier based on depth
    if room_num < 3:
        pool  = REGULAR_ENEMIES[:4]   # tier 1
        count = 3
    elif room_num < 6:
        pool  = REGULAR_ENEMIES[4:8]  # tier 2
        count = 4
    else:
        pool  = REGULAR_ENEMIES[8:]   # tier 3
        count = 5
    spawns = coords[:]
    result = []
    for i in range(count):
        data  = choice(pool)
        sx, sy = spawns[i%len(spawns)]
        result.append(Enemy(sx+randint(-30, 30), sy+randint(-30, 30),data))
    return result

pygame.init()
#initial screen
screen = pygame.display.set_mode((w_width,w_height))
clock = pygame.time.Clock()
#set title
pygame.display.set_caption(title)
#load backgrounds
bg = [
    pygame.transform.scale(pygame.image.load("assets/tilesets/tier1.png").convert(), (w_width, w_height)),
    pygame.transform.scale(pygame.image.load("assets/tilesets/tier2.png").convert(), (w_width, w_height)),
    pygame.transform.scale(pygame.image.load("assets/tilesets/tier3.png").convert(), (w_width, w_height)),
]
#initialize player class
player = Player(640, 360, "akira/akira_sprites_transparent_hires", CHARACTER_TEMPLATES["Akira"])
current_room = 0
enemies = generate_room(current_room)
door_rect = pygame.Rect(w_width - tile_size, w_height//2 - 40, tile_size, 80)
door_open = False

while True:
    dt = clock.tick(fps)/1000.0
    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == kset["attack"]:
                player.attack()
                atk = player.attacks[0]
                for enemy in enemies:
                    attack_range = player.player_rect.inflate(60, 60)
                    if attack_range.colliderect(enemy.rect):
                        enemy.hp -= randint(atk["damage"][0], atk["damage"][1])
                enemies = [e for e in enemies if e.hp>0]
                
            if event.key == kset["special1"]:
                atk = player.attacks[1]
                if player.spattack(0):
                    for enemy in enemies:
                        attack_range = player.player_rect.inflate(80, 80)
                        if attack_range.colliderect(enemy.rect):
                            enemy.hp -= randint(atk["damage"][0], atk["damage"][1])
                enemies = [e for e in enemies if e.hp>0]
                
            if event.key == kset["special2"]:
                atk = player.attacks[2]
                if player.spattack(1):
                    for enemy in enemies:
                        attack_range = player.player_rect.inflate(80, 80)
                        if attack_range.colliderect(enemy.rect):
                            enemy.hp -= randint(atk["damage"][0], atk["damage"][1])
                enemies = [e for e in enemies if e.hp>0]
                
            if event.key == kset["special3"]:
                atk = player.attacks[3]
                if player.special(2):
                    for enemy in enemies:
                        attack_range = player.player_rect.inflate(80, 80)
                        if attack_range.colliderect(enemy.rect):
                            enemy.hp -= randint(atk["damage"][0], atk["damage"][1])
                enemies = [e for e in enemies if e.hp>0]
                
            if event.key == kset["special4"]:
                atk = player.attacks[4]
                if player.special(3):
                    for enemy in enemies:
                        attack_range = player.player_rect.inflate(80, 80)
                        if attack_range.colliderect(enemy.rect):
                            enemy.hp -= randint(atk["damage"][0], atk["damage"][1])
                enemies = [e for e in enemies if e.hp>0]
                
    #updation
    keys = pygame.key.get_pressed()
    player.update(keys, wall_rects, dt)
    for enemy in enemies:
        player.hp -= enemy.update(player.player_rect, enemies, dt)
    #player death
    if player.hp <= 0:
        player.hp = player.max_hp
        player.player_rect.center = (640,360)
        current_room = 0
        enemies = generate_room(current_room)
        door_open = False
    #draw
    draw(screen, current_room)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    #door managament
    if len(enemies) == 0:
        door_open = True
    if door_open:
        pygame.draw.rect(screen, (200, 150, 50), door_rect)
    else:
        pygame.draw.rect(screen, (60, 40, 20), door_rect)
    if door_open:
        near_door = (player.player_rect.right >= w_width - tile_size - 5 and
                     door_rect.top < player.player_rect.centery < door_rect.bottom)
        if near_door:
            current_room += 1
            enemies = generate_room(current_room)
            door_open = False
            player.player_rect.center = (640, 360)
    pygame.display.update()
