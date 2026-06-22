from engine.game_loop import fps, w_width, w_height, title
from engine.input_handler import kset
from game_logic import main_menu
from sys import exit
import pygame

pygame.init()
screen = pygame.display.set_mode((w_width,w_height))
clock = pygame.time.Clock()
pygame.display.set_caption(title)
player = pygame.Surface((40,60))
player.fill((20,30,40))
player_rect = player.get_rect(center = (40,360))

while True:
    dt = clock.tick(fps)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    keys = pygame.key.get_pressed()
    if keys[kset["right"]]:
        player_rect.x += 300*dt
    if keys[kset["left"]]:
        player_rect.x -= 300*dt
    if keys[kset["up"]]:
        player_rect.y -= 300*dt
    if keys[kset["down"]]:
        player_rect.y += 300*dt
    
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > w_width:
        player_rect.right = w_width
    if player_rect.top < 0:
        player_rect.top = 0
    if player_rect.bottom > w_height:
        player_rect.bottom = w_height
    screen.fill((0,0,50))
    screen.blit(player, player_rect)
    
    pygame.display.update()

