"""
EnemySprite
───────────
Pygame sprite wrapping a models.Enemy instance.

AI state machine:
  IDLE → PATROL → CHASE → ATTACK → STAGGER → CHASE …
                    ↑
                    └─ enters when player is within AGGRO_RANGE

Week 2:  basic chase + attack
Week 3:  patrol waypoints, proper stagger knockback
Week 4:  real sprite sheet animations
"""
import pygame
import random
from models import Enemy as EnemyModel


class AIState:
    IDLE    = "idle"
    PATROL  = "patrol"
    CHASE   = "chase"
    ATTACK  = "attack"
    STAGGER = "stagger"
    DEATH   = "death"


class EnemySprite(pygame.sprite.Sprite):
    SPEED            = 80    # pixels per second
    AGGRO_RANGE      = 200   # px — distance at which enemy starts chasing
    ATTACK_RANGE     = 45    # px — distance at which enemy swings
    ATTACK_COOLDOWN  = 1.2   # seconds between attacks
    STAGGER_DURATION = 0.4   # seconds of stagger after taking a hit

    def __init__(self, model: EnemyModel, x: int, y: int):
        super().__init__()
        self.model  = model
        self.state  = AIState.IDLE
        self.facing = "left"

        self._attack_timer  = 0.0
        self._stagger_timer = 0.0

        # TODO (Week 4): replace with real sprite sheet
        self.image = pygame.Surface((32, 48), pygame.SRCALPHA)
        self.image.fill((220, 60, 60))           # placeholder: red rectangle
        self.rect      = self.image.get_rect(topleft=(x, y))
        self.hurt_rect = self.rect.inflate(-6, -6)

    # ── Public API ────────────────────────────────────────────────────────────

    def take_damage(self, amount: int) -> None:
        self.model.hp = max(0, self.model.hp - amount)
        if self.model.is_alive():
            self.state          = AIState.STAGGER
            self._stagger_timer = self.STAGGER_DURATION
        else:
            self.state = AIState.DEATH

    @property
    def is_dead(self) -> bool:
        return not self.model.is_alive()

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float, player_rect: pygame.Rect = None,
               walls: list = None) -> int:
        """
        Returns the damage dealt to the player this frame (0 if no hit).
        """
        self._attack_timer  = max(0, self._attack_timer  - dt)
        self._stagger_timer = max(0, self._stagger_timer - dt)

        if self.state == AIState.STAGGER:
            if self._stagger_timer == 0:
                self.state = AIState.CHASE
            return 0

        if self.state == AIState.DEATH:
            return 0

        if player_rect is None:
            return 0

        dist = pygame.math.Vector2(
            player_rect.centerx - self.rect.centerx,
            player_rect.centery - self.rect.centery,
        )
        distance = dist.length()

        # ── Attack ────────────────────────────────────────────────────────────
        if distance <= self.ATTACK_RANGE and self._attack_timer == 0:
            self.state         = AIState.ATTACK
            self._attack_timer = self.ATTACK_COOLDOWN
            available = self.model.available_attack_indices() or [0]
            idx    = random.choice(available)
            attack = self.model.attacks[idx]
            return random.randint(*attack["damage"])

        # ── Chase ─────────────────────────────────────────────────────────────
        elif distance <= self.AGGRO_RANGE:
            self.state     = AIState.CHASE
            direction      = dist.normalize()
            self.rect.x   += int(direction.x * self.SPEED * dt)
            self.rect.y   += int(direction.y * self.SPEED * dt)
            self.facing    = "left" if direction.x < 0 else "right"

        else:
            self.state = AIState.IDLE

        self.hurt_rect.center = self.rect.center
        return 0

    def draw(self, surface: pygame.Surface, camera=None) -> None:
        rect = camera.apply(self.rect) if camera else self.rect
        surface.blit(self.image, rect)
