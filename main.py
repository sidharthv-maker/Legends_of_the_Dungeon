from engine.game_loop import fps, w_width, w_height, title
from engine.input_handler import kset
from world.tilemap import draw as draw_map, wall_rects
from game_logic import main_menu
from sprites.player import Player
from sys import exit
import pygame

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
    draw_map(screen)
    player.draw(screen)
    pygame.display.update()

