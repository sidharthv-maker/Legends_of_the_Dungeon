fps = 60
w_width= 1280
w_height = 720
title = "Legends of the Dungeon"
tile_size = 32

from game_logic import main_menu
from sys import exit
import pygame

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.player = pygame.Surface((40,60))
        self.player.fill((20,30,40))
        self.player_rect = self.player.get_rect(center = (x,y))
        self.speed = 300
        
    def update(self,keys,wall_rects,dt):
        #move right
        if keys[kset["right"]] or keys[kset["righta"]]:
            self.player_rect.x += self.speed*dt
            for wall in wall_rects:
                if self.player_rect.colliderect(wall):
                    self.player_rect.right = wall.left
        #move left
        if keys[kset["left"]] or keys[kset["lefta"]]:
            self.player_rect.x -= self.speed*dt
            for wall in wall_rects:
                if self.player_rect.colliderect(wall):
                    self.player_rect.left = wall.right
        #move up
        if keys[kset["up"]] or keys[kset["upa"]]:
            self.player_rect.y -= self.speed*dt
            for wall in wall_rects:
                if self.player_rect.colliderect(wall):
                    self.player_rect.top = wall.bottom
        #move down
        if keys[kset["down"]] or keys[kset["downa"]]:
            self.player_rect.y += self.speed*dt
            for wall in wall_rects:
                if self.player_rect.colliderect(wall):
                    self.player_rect.bottom = wall.top
    
    def draw(self,screen):
        screen.blit(self.player, self.player_rect)

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
player = Player(640, 360)

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

