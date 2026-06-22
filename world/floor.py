"""
FloorScene
───────────
A complete dungeon floor — owns the game loop for actual gameplay.

Room sequence per floor:
    maps/floor_N/room_1.tmx
    maps/floor_N/room_2.tmx
    maps/floor_N/boss.tmx      ← always last

When all rooms are cleared:
  - player.floor increments
  - game auto-saves
  - loads floor_(N+1) or shows Victory screen if final floor done

Week 1:  player moves through a placeholder room
Week 2:  combat active, HUD showing
Week 3:  room sequencing + auto-save on floor clear
Week 4:  fade transitions between rooms, background music per floor
"""
import os
import pygame

from engine.scene_manager import Scene, SceneManager
from engine.camera        import Camera
from engine.input_handler import InputHandler
from engine.game_loop     import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE
from world.room           import Room
from sprites.player       import PlayerSprite
from ui.hud               import HUD
from models               import Player as PlayerModel

MAPS_DIR    = os.path.join(os.path.dirname(__file__), "..", "maps")
FINAL_FLOOR = 3      # game ends after clearing this floor
DARK        = (10, 10, 20)


class FloorScene(Scene):
    ROOM_FILES = ["room_1.tmx", "room_2.tmx", "boss.tmx"]

    def __init__(self, manager: SceneManager, player_model: PlayerModel):
        super().__init__(manager)
        self.player_model = player_model
        self.floor_number = player_model.floor
        self.room_index   = 0

        self.input = InputHandler()
        self.hud   = HUD(manager.screen)

        self._load_room()

    # ── Room management ───────────────────────────────────────────────────────

    def _room_path(self) -> str:
        filename = self.ROOM_FILES[self.room_index]
        return os.path.join(MAPS_DIR, f"floor_{self.floor_number}", filename)

    def _load_room(self) -> None:
        self.room = Room(self._room_path(), self.floor_number)

        # Spawn player in the centre of the map
        cx = self.room.tilemap.width  // 2 - TILE_SIZE
        cy = self.room.tilemap.height // 2
        self.player = PlayerSprite(self.player_model, cx, cy)

        self.camera = Camera(
            map_width=self.room.tilemap.width,
            map_height=self.room.tilemap.height,
            view_width=WINDOW_WIDTH,
            view_height=WINDOW_HEIGHT,
        )

    def _advance(self) -> None:
        """Move to the next room or next floor."""
        self.room_index += 1

        if self.room_index >= len(self.ROOM_FILES):
            # Floor complete
            self.player_model.floor += 1
            self.room_index = 0

            from save_system import save_game
            save_game(self.player_model)

            if self.player_model.floor > FINAL_FLOOR:
                # Game won
                from ui.game_over import GameOver
                self.manager.replace(GameOver(self.manager, self.player_model, won=True))
                return

            self.floor_number = self.player_model.floor

        self._load_room()

    # ── Scene interface ───────────────────────────────────────────────────────

    def handle_events(self, events: list) -> None:
        self.input.update(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # TODO (Week 4): push PauseMenu scene
                pass

    def update(self, dt: float) -> None:
        # Trigger attack
        if self.input.just_pressed("attack"):
            self.player.start_attack()

        # Use potion
        if self.input.just_pressed("use_potion"):
            import random
            if self.player_model.potions > 0:
                heal = random.randint(25, 40)
                self.player_model.heal(heal)
                self.player_model.potions -= 1

        self.player.update(dt, self.input, self.room.tilemap.wall_rects)
        self.room.update(dt, self.player)
        self.camera.follow(self.player.rect.center)

        # Room cleared
        if self.room.complete:
            self._advance()

        # Player died
        if self.player.is_dead:
            from ui.game_over import GameOver
            self.manager.replace(
                GameOver(self.manager, self.player_model, won=False))

    def draw(self) -> None:
        screen = self.manager.screen
        screen.fill(DARK)

        self.room.draw(screen, self.camera)
        self.player.draw(screen, self.camera)

        # Pass the nearest alive enemy to the HUD for its health bar
        alive = [e for e in self.room.enemies if not e.is_dead]
        self.hud.draw(self.player_model, alive[0].model if alive else None)
