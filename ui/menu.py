"""
MainMenu
────────
First scene the player sees on launch.

Options:
  New Game  → CharacterSelect scene
  Load Game → loads save file, jumps straight into FloorScene
  Quit      → exits the game

Controls: UP / DOWN to navigate, ENTER or J to confirm.

Week 4:  background art, title logo sprite, animated title text
"""
import pygame
from engine.scene_manager import Scene, SceneManager
from save_system import load_game

WHITE  = (255, 255, 255)
YELLOW = (255, 215,   0)
GREY   = (120, 120, 120)
DARK   = ( 20,  20,  40)


class MainMenu(Scene):
    OPTIONS = ["New Game", "Load Game", "Quit"]

    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.font_title  = pygame.font.SysFont("monospace", 46, bold=True)
        self.font_option = pygame.font.SysFont("monospace", 28)
        self.font_hint   = pygame.font.SysFont("monospace", 14)
        self.selected    = 0

    def handle_events(self, events: list) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_RETURN, pygame.K_j):
                self._confirm()

    def _confirm(self) -> None:
        choice = self.OPTIONS[self.selected]
        if choice == "New Game":
            from ui.character_select import CharacterSelect
            self.manager.push(CharacterSelect(self.manager))
        elif choice == "Load Game":
            player = load_game()
            if player:
                from world.floor import FloorScene
                self.manager.replace(FloorScene(self.manager, player))
        elif choice == "Quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        screen = self.manager.screen
        screen.fill(DARK)
        cx = screen.get_width() // 2

        # Title
        title = self.font_title.render("LEGENDS OF THE DUNGEON", True, YELLOW)
        screen.blit(title, (cx - title.get_width() // 2, 170))

        # Menu options
        for i, opt in enumerate(self.OPTIONS):
            color  = YELLOW if i == self.selected else WHITE
            prefix = "▶  " if i == self.selected else "   "
            text   = self.font_option.render(prefix + opt, True, color)
            screen.blit(text, (cx - 120, 310 + i * 55))

        # Controls hint
        hint = self.font_hint.render(
            "↑ / ↓  navigate      ENTER  confirm", True, GREY)
        screen.blit(hint, (cx - hint.get_width() // 2, screen.get_height() - 40))
