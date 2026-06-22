import pygame
from engine.input_handler import kset
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