fps = 60
w_width= 1280
w_height = 720
title = "Legends of the Dungeon"
tile_size = 32

from sys import exit
from random import randint, choice
import pygame
import math
from data import REGULAR_ENEMIES, BOSSES

class Player:
    def __init__(self, x, y, name):
        def load(filename):
            img = pygame.image.load(f"assets/sprites/player/{name}/{filename}").convert_alpha()
            return pygame.transform.scale(img,(3*img.get_width(), 3*img.get_height()))
        self.anims = {
            "idle_left":  [load("05_idle_left_01.png"),  load("06_idle_left_02.png")],
            "idle_right": [load("07_idle_right_01.png"), load("08_idle_right_02.png")],
            "idle_front": [load("02_main_front.png")],
            "idle_back":  [load("04_main_back.png")],
            "walk_left":  [load("09_walk_left_01.png"),  load("10_walk_left_02.png"),  load("11_walk_left_03.png")],
            "walk_right": [load("12_walk_right_01.png"), load("13_walk_right_02.png"), load("14_walk_right_03.png")],
            "attack_right":  [load("15_basic_left_01.png"), load("16_basic_left_02_slash.png")],
            "attack_left": [load("17_basic_right_01_slash.png"), load("18_basic_right_02.png")],
        }
        self.speed = 300
        self.facing = "right"
        self.state = "idle"
        self.attacking = False
        self.anim_frame = 0
        self.anim_timer = 0
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
                
    def attack(self):
        if self.facing not in ("left", "right"):
            return
        self.attacking = True
        self.anim_frame = 0
        self.anim_timer = 0
        self.current_anim_key = "attack_" + self.facing
        
    
    def draw(self, screen):
        current_anim = self.anims[self.current_anim_key]
        screen.blit(current_anim[self.anim_frame],self.player_rect)

class Enemy:
    def __init__(self, x, y, data):
        self.name    = data["name"]
        self.max_hp  = data["max_hp"]
        self.hp      = data["max_hp"]
        self.speed   = 150
        self.surf    = pygame.Surface((40, 60))
        self.surf.fill((180, 60, 60))
        self.rect    = self.surf.get_rect(center=(x, y))

    def update(self, player_rect, enemies, dt):
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        dis = math.sqrt(dx*dx + dy*dy)
        if dis != 0:
            dx /= dis
            dy /= dis
        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt
        # separate from other enemies
        for other in enemies:
            if other is not self and self.rect.colliderect(other.rect):
                ox = self.rect.centerx - other.rect.centerx
                oy = self.rect.centery - other.rect.centery
                od = math.sqrt(ox*ox + oy*oy)
                if od != 0:
                    self.rect.x += (ox / od) * 2
                    self.rect.y += (oy / od) * 2

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        bar_width  = 50
        bar_height = 6
        bar_x = self.rect.x
        bar_y = self.rect.y - 12
        pygame.draw.rect(screen, (80, 0, 0),   (bar_x, bar_y, bar_width, bar_height))
        current_width = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(screen, (200, 0, 0),  (bar_x, bar_y, current_width, bar_height))

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

def draw(screen):
    screen.fill((80,60,50))
    for wall in wall_rects:
        pygame.draw.rect(screen,(40,30,20),wall)

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
screen = pygame.display.set_mode((w_width,w_height))#
clock = pygame.time.Clock()
#set title
pygame.display.set_caption(title)
#initialize player class
player = Player(640, 360, "larry")
current_room = 0
enemies = generate_room(current_room)
door_rect = pygame.Rect(w_width - tile_size, w_height//2 - 40, tile_size, 80)
door_open = False

while True:
    dt = clock.tick(fps)/1000.0
    for event in pygame.event.get():
        #exit condition
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == kset["attack"]:
                player.attack()
                for enemy in enemies:
                    if enemy:
                        attack_range = player.player_rect.inflate(60, 60)
                        if attack_range.colliderect(enemy.rect):
                            enemy.hp -= 20
            enemies = [e for e in enemies if e.hp > 0]
    #adds "event listeners" for various keys
    keys = pygame.key.get_pressed()
    #move player
    player.update(keys, wall_rects, dt)
    #display player
    draw(screen)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
        enemy.update(player.player_rect, enemies, dt)
    # room cleared
    if len(enemies) == 0:
        door_open = True
    # draw door
    if door_open:
        pygame.draw.rect(screen, (200, 150, 50), door_rect)
    else:
        pygame.draw.rect(screen, (60, 40, 20), door_rect)
    # next room — player pressed against right wall and aligned with door
    if door_open:
        near_door = (player.player_rect.right >= w_width - tile_size - 5 and
                     door_rect.top < player.player_rect.centery < door_rect.bottom)
        if near_door:
            current_room += 1
            enemies = generate_room(current_room)
            door_open = False
            player.player_rect.center = (640, 360)
    pygame.display.update()

