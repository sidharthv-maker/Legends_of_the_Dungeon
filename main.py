from game_logic import main_menu
from sys import exit
import pygame
# if __name__ == "__main__":
#     main_menu()

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
pygame.display.set_caption("Legends of the Dungeon")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.fill((0,0,50))
    pygame.display.update()
    clock.tick(60)
