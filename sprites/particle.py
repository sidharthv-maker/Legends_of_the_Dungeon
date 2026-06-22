"""
Particle & ParticleSystem
──────────────────────────
Lightweight visual effects — no gameplay impact.

Built-in presets:
  system.hit_sparks(pos)    → small yellow sparks when a hit lands
  system.death_burst(pos)   → large red burst when an enemy dies
  system.coin_pop(pos)      → gold coins arc upward on gold pickup

Usage:
    particles = ParticleSystem()

    # each frame:
    particles.update(dt)
    particles.draw(screen, camera)

    # on a hit:
    particles.hit_sparks(enemy.rect.center)

Week 4:  wire into Room combat callbacks
"""
import pygame
import random
import math


class Particle:
    def __init__(self, x: float, y: float,
                 vx: float, vy: float,
                 color: tuple,
                 size: float,
                 lifetime: float):
        self.x        = x
        self.y        = y
        self.vx       = vx
        self.vy       = vy
        self.color    = color
        self.size     = size
        self.lifetime = lifetime   # total seconds this particle lives
        self.age      = 0.0

    @property
    def alive(self) -> bool:
        return self.age < self.lifetime

    def update(self, dt: float) -> None:
        self.x   += self.vx * dt
        self.y   += self.vy * dt
        self.vy  += 400 * dt   # gravity pulls particles down
        self.age += dt


class ParticleSystem:
    def __init__(self):
        self.particles: list = []

    def spawn(self, particle: Particle) -> None:
        self.particles.append(particle)

    def update(self, dt: float) -> None:
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update(dt)

    def draw(self, surface: pygame.Surface, camera=None) -> None:
        for p in self.particles:
            x = p.x - (camera.offset.x if camera else 0)
            y = p.y - (camera.offset.y if camera else 0)
            # Shrink radius as particle ages
            ratio  = max(0.0, 1.0 - (p.age / p.lifetime))
            radius = max(1, int(p.size * ratio))
            pygame.draw.circle(surface, p.color, (int(x), int(y)), radius)

    # ── Preset factories ──────────────────────────────────────────────────────

    def hit_sparks(self, pos: tuple, count: int = 8) -> None:
        """Small yellow sparks when a hit lands."""
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(60, 180)
            self.spawn(Particle(
                x=pos[0], y=pos[1],
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed - 50,
                color=random.choice([
                    (255, 230, 50), (255, 180, 30), (255, 255, 150)
                ]),
                size=random.uniform(2, 5),
                lifetime=random.uniform(0.2, 0.5),
            ))

    def death_burst(self, pos: tuple, count: int = 20) -> None:
        """Larger burst when an enemy dies."""
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(80, 260)
            self.spawn(Particle(
                x=pos[0], y=pos[1],
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed - 80,
                color=random.choice([
                    (220, 50, 50), (255, 100, 30), (200, 30, 30)
                ]),
                size=random.uniform(3, 8),
                lifetime=random.uniform(0.4, 0.9),
            ))

    def coin_pop(self, pos: tuple, count: int = 6) -> None:
        """Gold coins arc upward on gold pickup."""
        for _ in range(count):
            angle = random.uniform(math.pi * 1.1, math.pi * 1.9)   # upward arc
            speed = random.uniform(100, 220)
            self.spawn(Particle(
                x=pos[0], y=pos[1],
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                color=random.choice([
                    (255, 215, 0), (255, 200, 50), (230, 190, 20)
                ]),
                size=random.uniform(4, 7),
                lifetime=random.uniform(0.5, 0.8),
            ))
