"""
CharacterSelect
────────────────
Reads CHARACTER_TEMPLATES from data.py automatically.
No changes needed here when new heroes are added to data.py.

Controls: LEFT / RIGHT to browse, ENTER or J to confirm, ESC to go back.

Week 4:  character preview art, animated selection highlight
"""
import pygame
from engine.scene_manager import Scene, SceneManager
from data import CHARACTER_TEMPLATES
from models import Player as PlayerModel

WHITE  = (255, 255, 255)
YELLOW = (255, 215,   0)
GREY   = (160, 160, 160)
DARK   = ( 20,  20,  40)
DIM    = ( 40,  40,  70)


class CharacterSelect(Scene):
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.font_title  = pygame.font.SysFont("monospace", 34, bold=True)
        self.font_name   = pygame.font.SysFont("monospace", 26, bold=True)
        self.font_stat   = pygame.font.SysFont("monospace", 18)
        self.font_hint   = pygame.font.SysFont("monospace", 14)
        self.names       = list(CHARACTER_TEMPLATES.keys())
        self.selected    = 0

    @property
    def _template(self) -> dict:
        return CHARACTER_TEMPLATES[self.names[self.selected]]

    def handle_events(self, events: list) -> None:
        for event in events:
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_LEFT:
                self.selected = (self.selected - 1) % len(self.names)
            elif event.key == pygame.K_RIGHT:
                self.selected = (self.selected + 1) % len(self.names)
            elif event.key in (pygame.K_RETURN, pygame.K_j):
                self._confirm()
            elif event.key == pygame.K_ESCAPE:
                self.manager.pop()

    def _confirm(self) -> None:
        name = self.names[self.selected]
        t    = CHARACTER_TEMPLATES[name]
        player = PlayerModel(
            name=name,
            title=t["title"],
            max_hp=t["max_hp"],
            attacks=t["attacks"],
        )
        from world.floor import FloorScene
        self.manager.replace(FloorScene(self.manager, player))

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> None:
        screen = self.manager.screen
        screen.fill(DARK)
        cx = screen.get_width() // 2
        t  = self._template

        # Title
        title = self.font_title.render("CHOOSE YOUR HERO", True, YELLOW)
        screen.blit(title, (cx - title.get_width() // 2, 55))

        # Hero name + title
        name_str = f"{self.names[self.selected]}  —  {t['title']}"
        name_surf = self.font_name.render(name_str, True, WHITE)
        screen.blit(name_surf, (cx - name_surf.get_width() // 2, 150))

        # TODO (Week 4): draw character preview sprite here

        # Stats panel
        strongest = t["attacks"][-1]
        stats = [
            f"Max HP      :  {t['max_hp']}",
            f"Attacks     :  {len(t['attacks'])}",
            f"Strongest   :  {strongest['name']}",
            f"  damage    :  {strongest['damage'][0]} – {strongest['damage'][1]}",
        ]
        panel_x = cx - 200
        for i, line in enumerate(stats):
            s = self.font_stat.render(line, True, GREY)
            screen.blit(s, (panel_x, 220 + i * 30))

        # Page indicator
        idx = self.font_stat.render(
            f"{self.selected + 1}  /  {len(self.names)}", True, YELLOW)
        screen.blit(idx, (cx - idx.get_width() // 2, 380))

        # Navigation hint
        hint = self.font_hint.render(
            "◀ / ▶  browse      ENTER  confirm      ESC  back", True, GREY)
        screen.blit(hint, (cx - hint.get_width() // 2, screen.get_height() - 40))
