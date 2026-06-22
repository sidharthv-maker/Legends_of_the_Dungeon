"""
PlayerSprite
────────────
Pygame sprite that wraps a models.Player instance.

Owns:
  - Animation state machine  (idle / walk / attack / hurt / death)
  - body rect   (position + size, used for world collision)
  - hurt rect   (slightly smaller, where incoming damage is received)
  - attack rect (appears during attack frames, deals damage to enemies)

Week 1:  movement + tilemap collision
Week 2:  attack frames + hurt box + i-frames
Week 3:  loot pickup, floor interaction
Week 4:  real sprite sheet animations replacing coloured rectangles
"""
import pygame
from models import Player as PlayerModel


class AnimState:
    IDLE   = "idle"
    WALK   = "walk"
    ATTACK = "attack"
    HURT   = "hurt"
    DEATH  = "death"


class PlayerSprite(pygame.sprite.Sprite):
    SPEED            = 200   # pixels per second
    ATTACK_DURATION  = 0.35  # seconds the attack window stays open
    IFRAMES_DURATION = 0.6   # invincibility seconds after getting hit

    def __init__(self, model: PlayerModel, x: int, y: int):
        super().__init__()
        self.model   = model
        self.state   = AnimState.IDLE
        self.facing  = "right"   # "left" | "right" | "up" | "down"
        self.velocity = pygame.math.Vector2(0, 0)

        # ── Timers ────────────────────────────────────────────────────────────
        self._attack_timer = 0.0
        self._iframe_timer = 0.0

        # ── Rects ─────────────────────────────────────────────────────────────
        # TODO (Week 4): replace Surface with a real loaded sprite sheet
        self.image = pygame.Surface((32, 48), pygame.SRCALPHA)
        self.image.fill((70, 130, 255))           # placeholder: blue rectangle
        self.rect        = self.image.get_rect(topleft=(x, y))
        self.hurt_rect   = self.rect.inflate(-8, -8)
        self.attack_rect = pygame.Rect(0, 0, 0, 0)   # active only during attack frames

    # ── Public API ────────────────────────────────────────────────────────────

    def take_damage(self, amount: int) -> None:
        """Apply damage if not currently in i-frames."""
        if self._iframe_timer > 0:
            return
        self.model.hp  = max(0, self.model.hp - amount)
        self._iframe_timer = self.IFRAMES_DURATION
        self.state = AnimState.HURT if self.model.is_alive() else AnimState.DEATH

    def start_attack(self) -> None:
        """Trigger an attack. Ignored if already attacking or dead."""
        if self.state in (AnimState.ATTACK, AnimState.DEATH):
            return
        self.state         = AnimState.ATTACK
        self._attack_timer = self.ATTACK_DURATION
        self._set_attack_rect()

    @property
    def is_attacking(self) -> bool:
        return self.state == AnimState.ATTACK

    @property
    def is_dead(self) -> bool:
        return not self.model.is_alive()

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self, dt: float, input_handler=None, walls: list = None) -> None:
        """
        dt            – seconds since last frame
        input_handler – InputHandler instance (or None for no input)
        walls         – list of pygame.Rect wall tiles for collision
        """
        self._iframe_timer = max(0, self._iframe_timer - dt)
        self._attack_timer = max(0, self._attack_timer - dt)

        # Clear attack rect when animation ends
        if self._attack_timer == 0 and self.state == AnimState.ATTACK:
            self.state = AnimState.IDLE
            self.attack_rect = pygame.Rect(0, 0, 0, 0)

        # Don't move while attacking or dead
        if self.state in (AnimState.ATTACK, AnimState.DEATH):
            return

        # Movement from input
        if input_handler:
            vec = input_handler.movement_vector()
            self.velocity = vec * self.SPEED
            self.state    = AnimState.WALK if vec.length() > 0 else AnimState.IDLE
            if vec.x > 0:   self.facing = "right"
            elif vec.x < 0: self.facing = "left"
            elif vec.y > 0: self.facing = "down"
            elif vec.y < 0: self.facing = "up"

        self._move_and_collide(dt, walls or [])
        self.hurt_rect.center = self.rect.center

    # ── Private helpers ───────────────────────────────────────────────────────

    def _move_and_collide(self, dt: float, walls: list) -> None:
        """Axis-separated collision so corners don't get stuck."""
        self.rect.x += int(self.velocity.x * dt)
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity.x > 0: self.rect.right = wall.left
                else:                    self.rect.left  = wall.right

        self.rect.y += int(self.velocity.y * dt)
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.velocity.y > 0: self.rect.bottom = wall.top
                else:                   self.rect.top    = wall.bottom

    def _set_attack_rect(self) -> None:
        """Position the attack hitbox in front of the player."""
        w, h = 40, 32
        if self.facing == "right":
            self.attack_rect = pygame.Rect(self.rect.right, self.rect.centery - h // 2, w, h)
        elif self.facing == "left":
            self.attack_rect = pygame.Rect(self.rect.left - w, self.rect.centery - h // 2, w, h)
        elif self.facing == "down":
            self.attack_rect = pygame.Rect(self.rect.centerx - h // 2, self.rect.bottom, h, w)
        else:
            self.attack_rect = pygame.Rect(self.rect.centerx - h // 2, self.rect.top - w, h, w)

    def draw(self, surface: pygame.Surface, camera=None) -> None:
        rect = camera.apply(self.rect) if camera else self.rect
        surface.blit(self.image, rect)

        # Debug: draw attack rect in yellow (remove in Week 4)
        if self.is_attacking and camera:
            pygame.draw.rect(surface, (255, 255, 0),
                             camera.apply(self.attack_rect), 1)
