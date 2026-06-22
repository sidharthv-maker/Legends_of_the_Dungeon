"""
Room
─────
One dungeon room:  a TileMap + its enemy sprites + particle system.

Lifecycle:
  1. Room spawns enemies from the TileMap's "Objects" layer.
  2. FloorScene calls room.update() every frame.
  3. When all enemies are dead → room.complete = True.
  4. FloorScene reads room.complete and loads the next room.

Week 2:  enemy spawn + combat loop
Week 3:  loot drops, door trigger object
Week 4:  wire particle presets to every hit/death/pickup
"""
import random
import pygame

from world.tilemap    import TileMap
from sprites.player   import PlayerSprite
from sprites.enemy    import EnemySprite
from sprites.boss     import BossSprite
from sprites.particle import ParticleSystem
from game_logic       import generate_enemy_for_floor


class Room:
    def __init__(self, tmx_path: str, floor_number: int):
        self.tilemap      = TileMap(tmx_path)
        self.floor_number = floor_number
        self.enemies:     list = []
        self.particles    = ParticleSystem()
        self.complete     = False   # True once every enemy is dead

        self._spawn_enemies()

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _spawn_enemies(self) -> None:
        for sp in self.tilemap.spawn_points:
            if sp["type"] not in ("enemy_spawn", "boss_spawn"):
                continue
            model = generate_enemy_for_floor(self.floor_number)
            if sp["type"] == "boss_spawn" or model.is_boss:
                sprite = BossSprite(model, sp["x"], sp["y"])
            else:
                sprite = EnemySprite(model, sp["x"], sp["y"])
            self.enemies.append(sprite)

    # ── Per-frame ─────────────────────────────────────────────────────────────

    def update(self, dt: float, player: PlayerSprite) -> None:
        walls = self.tilemap.wall_rects

        # ── Enemy AI + enemy → player damage ──────────────────────────────────
        for enemy in self.enemies:
            if enemy.is_dead:
                continue
            dmg = enemy.update(dt, player.rect, walls)
            if dmg > 0:
                player.take_damage(dmg)

        # ── Player attack → enemy hit detection ───────────────────────────────
        if player.is_attacking:
            for enemy in self.enemies:
                if enemy.is_dead:
                    continue
                if not player.attack_rect.colliderect(enemy.hurt_rect):
                    continue

                # TODO (Week 2): use player.model.attack_target() for real damage
                dmg      = random.randint(
                    player.model.attacks[0]["damage"][0],
                    player.model.attacks[0]["damage"][1],
                )
                was_alive = not enemy.is_dead
                enemy.take_damage(dmg)
                self.particles.hit_sparks(enemy.rect.center)

                if was_alive and enemy.is_dead:
                    # Give rewards to player model
                    player.model.gold    += enemy.model.reward_gold
                    player.model.potions += enemy.model.reward_potions
                    player.model.wins    += 1
                    if enemy.model.is_boss:
                        player.model.bosses_defeated += 1
                    self.particles.death_burst(enemy.rect.center)
                    self.particles.coin_pop(enemy.rect.center)

        self.particles.update(dt)

        # Room clears when all enemies are dead
        if self.enemies and all(e.is_dead for e in self.enemies):
            self.complete = True

    def draw(self, surface: pygame.Surface, camera=None) -> None:
        self.tilemap.draw(surface, camera)
        for enemy in self.enemies:
            if not enemy.is_dead:
                enemy.draw(surface, camera)
        self.particles.draw(surface, camera)
