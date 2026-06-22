"""
GameOver
─────────
Shown when the player dies or beats the final boss.

Displays:
  - Win or loss heading
  - Hero name
  - Floors cleared, enemies killed, bosses defeated, gold collected

Options:
  Try Again → CharacterSelect
  Main Menu → MainMenu

Controls: UP / DOWN to navigate, ENTER or J to confirm.

Week 4:  implement and wire in from FloorScene
"""
import pygame
from engine.scene_manager import Scene, SceneManager
from models import Player as PlayerModel

WHITE  = (255, 255, 255)
RED    = (210,  40,  40)
YELLOW = (255, 215,   0)
GREY   = (160, 160, 160)
DARK   = ( 20,  20,  40)


class GameOver(Scene):
    OPTIONS = ["Try Again", "Main Menu"]

    def __init__(self, manager: SceneManager,
                 player: PlayerModel, won: bool = False):
        super().__init__(manager)
        self.player   = player
        self.won      = won
        self.selected = 0

        self.font_big  = pygame.font.SysFont("monospace", 52, bold=True)
        self.font_stat = pygame.font.SysFont("monospace", 22)
        self.font_opt  = pygame.font.SysFont("monospace", 26)
        self.font_hint = pygame.font.SysFont("monospace", 14)

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
        if self.OPTIONS[self.selected] == "Try Again":
            from ui.character_select import CharacterSelect
            self.manager.replace(CharacterSelect(self.manager))
        else:
            from ui.menu import MainMenu
            self.manager.replace(MainMenu(self.manager))

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        screen = self.manager.screen
        screen.fill(DARK)
        cx = screen.get_width() // 2

        # Heading
        heading = "VICTORY!" if self.won else "YOU DIED"
        color   = YELLOW    if self.won else RED
        head    = self.font_big.render(heading, True, color)
        screen.blit(head, (cx - head.get_width() // 2, 90))

        # Stats
        p = self.player
        stats = [
            f"Hero             :  {p.full_name()}",
            f"Floors Cleared   :  {p.floor - 1}",
            f"Enemies Killed   :  {p.wins}",
            f"Bosses Defeated  :  {p.bosses_defeated}",
            f"Gold Collected   :  {p.gold}",
        ]
        for i, line in enumerate(stats):
            s = self.font_stat.render(line, True, GREY)
            screen.blit(s, (cx - s.get_width() // 2, 200 + i * 36))

        # Options
        for i, opt in enumerate(self.OPTIONS):
            col    = YELLOW if i == self.selected else WHITE
            prefix = "▶  " if i == self.selected else "   "
            t      = self.font_opt.render(prefix + opt, True, col)
            screen.blit(t, (cx - 90, 430 + i * 50))

        # Hint
        hint = self.font_hint.render(
            "↑ / ↓  navigate      ENTER  confirm", True, GREY)
        screen.blit(hint, (cx - hint.get_width() // 2, screen.get_height() - 40))
