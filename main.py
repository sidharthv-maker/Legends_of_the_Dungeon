fps = 60
w_width= 1280
w_height = 720
title = "Legends of the Dungeon"
tile_size = 32

from game_logic import main_menu
from sys import exit
import pygame
from random import randint
import math

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
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.hp = 100
        self.speed = 150
        self.surf = pygame.Surface((40,60))
        self.rect = self.surf.get_rect(center = (x,y))
    
    def update(self,player_rect,dt):
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        dis = math.sqrt(dx*dx+dy*dy)
        if dis != 0:
            dx /= dis
            dy /= dis
        self.rect.x += dx*self.speed*dt
        self.rect.y += dy*self.speed*dt
    
    def draw(self,screen):
        screen.blit(self.surf,self.rect)
        bar_width = 40
        bar_height = 6
        bar_x = self.rect.x
        bar_y = self.rect.y-15
        # background
        pygame.draw.rect(screen, (80, 0, 0), (bar_x,bar_y,bar_width,bar_height))
        # foreground - width shrinks as hp drops
        current_width = int(bar_width*(self.hp/100))
        pygame.draw.rect(screen, (200, 0, 0), (bar_x,bar_y,current_width,bar_height))
    

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

pygame.init()
#initial screen
screen = pygame.display.set_mode((w_width,w_height))#
clock = pygame.time.Clock()
#set title
pygame.display.set_caption(title)
#initialize player class
player = Player(640, 360, "larry")
enemies = [Enemy(randint(100,1180), randint(50,670)), Enemy(randint(100,1180), randint(50,670)), Enemy(randint(100,1180), randint(50,670))]

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
        if enemy:
            enemy.draw(screen)
            enemy.update(player.player_rect, dt) 
    pygame.display.update()

