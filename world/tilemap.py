import pygame
from engine.game_loop import tile_size
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
