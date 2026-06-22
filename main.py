"""
main.py  —  Legends of the Dungeon (pygame entry point)
─────────────────────────────────────────────────────────
Run:
    python main.py

To play the original console version:
    python -c "from game_logic import main_menu; main_menu()"
"""
import pygame
from engine.game_loop     import FPS, WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from engine.scene_manager import SceneManager
from ui.menu              import MainMenu


def main() -> None:
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock  = pygame.time.Clock()

    manager = SceneManager(screen)
    manager.push(MainMenu(manager))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0   # seconds since last frame

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        manager.handle_events(events)
        manager.update(dt)
        manager.draw()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
