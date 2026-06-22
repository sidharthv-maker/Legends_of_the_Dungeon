"""
HUD (Heads-Up Display)
──────────────────────
Drawn on top of everything — no camera offset applied.

Shows:
  - Player health bar + name          (top-left)
  - Active enemy health bar + name    (top-right)
  - Floor number                      (top-center)
  - Gold counter                      (below player bar)
  - Potion count                      (below gold)

Week 2:  health bars + gold
Week 3:  potion count + floor number
Week 4:  swap SysFont for a real pixel font from assets/fonts/
"""
import pygame
from models import Player as PlayerModel, Enemy as EnemyModel

# ── Colours ───────────────────────────────────────────────────────────────────
BAR_BG    = ( 60,  10,  10)
HP_GREEN  = ( 50, 200,  80)
HP_YELLOW = (220, 200,  30)
HP_RED    = (210,  30,  30)
GOLD_COL  = (255, 215,   0)
WHITE     = (255, 255, 255)
DARK      = ( 20,  20,  40)


def _hp_color(ratio: float) -> tuple:
    if ratio > 0.5:  return HP_GREEN
    if ratio > 0.25: return HP_YELLOW
    return HP_RED


class HUD:
    BAR_W = 220
    BAR_H = 18

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        # TODO (Week 4): load from assets/fonts/ e.g. "Press Start 2P"
        self.font  = pygame.font.SysFont("monospace", 14, bold=True)
        self.small = pygame.font.SysFont("monospace", 12)

    def draw(self, player: PlayerModel, enemy: EnemyModel = None) -> None:
        self._draw_player_bars(player)
        if enemy:
            self._draw_enemy_bar(enemy)
        self._draw_gold(player)
        self._draw_potions(player)
        self._draw_floor(player)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _draw_bar(self, x: int, y: int,
                  current: int, maximum: int, label: str) -> None:
        ratio  = current / maximum if maximum else 0
        filled = int(self.BAR_W * ratio)

        pygame.draw.rect(self.screen, BAR_BG,    (x, y, self.BAR_W, self.BAR_H))
        pygame.draw.rect(self.screen, _hp_color(ratio), (x, y, filled, self.BAR_H))
        pygame.draw.rect(self.screen, WHITE,     (x, y, self.BAR_W, self.BAR_H), 1)

        text = self.font.render(f"{label}  {current}/{maximum}", True, WHITE)
        self.screen.blit(text, (x + 4, y + 1))

    def _draw_player_bars(self, player: PlayerModel) -> None:
        self._draw_bar(10, 10, player.hp, player.max_hp, player.name)

    def _draw_enemy_bar(self, enemy: EnemyModel) -> None:
        x = self.screen.get_width() - self.BAR_W - 10
        self._draw_bar(x, 10, enemy.hp, enemy.max_hp, enemy.name)

    def _draw_gold(self, player: PlayerModel) -> None:
        text = self.font.render(f"Gold: {player.gold}", True, GOLD_COL)
        self.screen.blit(text, (10, 36))

    def _draw_potions(self, player: PlayerModel) -> None:
        text = self.font.render(f"Potions: {player.potions}", True, WHITE)
        self.screen.blit(text, (10, 54))

    def _draw_floor(self, player: PlayerModel) -> None:
        text = self.font.render(f"Floor {player.floor}", True, WHITE)
        cx   = self.screen.get_width() // 2
        self.screen.blit(text, (cx - text.get_width() // 2, 10))
