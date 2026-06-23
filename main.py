fps = 60
w_width= 1280
w_height = 720
title = "Legends of the Dungeon"
tile_size = 32

from game_logic import main_menu
from sys import exit
import pygame

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
        }
        self.speed = 300
        self.facing = "right"
        self.state = "idle"
        self.anim_frame = 0
        self.anim_timer = 0
        self.frame_duration = 0.15
        self.current_anim_key = "idle_right"
        self.player_rect = self.anims["idle_right"][0].get_rect(center=(x, y))

    def update(self, keys, wall_rects, dt):
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

    def draw(self, screen):
        current_anim = self.anims[self.current_anim_key]
        screen.blit(current_anim[self.anim_frame], self.player_rect)

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

while True:
    dt = clock.tick(fps)/1000.0
    for event in pygame.event.get():
        #exit condition
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #adds "event listeners" for various keys
    keys = pygame.key.get_pressed()
    #move player
    player.update(keys, wall_rects, dt)
    #display player
    draw(screen)
    player.draw(screen)
    pygame.display.update()

