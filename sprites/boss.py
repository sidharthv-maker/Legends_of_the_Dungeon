"""
BossSprite
──────────
Extends EnemySprite with:
  - Larger hitbox (64×80 instead of 32×48)
  - Phase 2 at 50% HP — gets faster, cooldown drops
  - Screen-shake trigger on slam attacks (Week 4)

Bosses are auto-detected from data.py (is_boss=True) and spawned by Room.

Week 3:  Phase 1 working
Week 4:  Phase 2 transition VFX + slam screen-shake
"""
import pygame
from sprites.enemy import EnemySprite, AIState
from models import Enemy as EnemyModel


class BossSprite(EnemySprite):
    SPEED            = 55
    AGGRO_RANGE      = 350
    ATTACK_RANGE     = 60
    ATTACK_COOLDOWN  = 1.8
    PHASE2_THRESHOLD = 0.5    # phase 2 triggers at 50% HP

    def __init__(self, model: EnemyModel, x: int, y: int):
        super().__init__(model, x, y)
        self.phase = 1

        # Bosses are visually bigger
        # TODO (Week 4): replace with real boss sprite sheet
        self.image = pygame.Surface((64, 80), pygame.SRCALPHA)
        self.image.fill((140, 0, 200))            # placeholder: purple rectangle
        self.rect      = self.image.get_rect(topleft=(x, y))
        self.hurt_rect = self.rect.inflate(-10, -10)

    # ── Phase check ───────────────────────────────────────────────────────────

    @property
    def in_phase2(self) -> bool:
        return (self.model.hp / self.model.max_hp) <= self.PHASE2_THRESHOLD

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float, player_rect: pygame.Rect = None,
               walls: list = None) -> int:

        # Transition to phase 2 once
        if self.phase == 1 and self.in_phase2:
            self.phase          = 2
            self.SPEED          = 80
            self.ATTACK_COOLDOWN = 1.0
            # TODO (Week 4): trigger screen-shake + particle burst here

        return super().update(dt, player_rect, walls)
