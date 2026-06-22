"""
TileMap
────────
Loads a Tiled .tmx file via pytmx and renders it to a surface.

Expected layers inside every .tmx:
  "Ground"   – floor tiles, drawn first, no collision
  "Walls"    – wall tiles, drawn on top, collision rects exposed
  "Objects"  – Tiled object layer:
                  type "enemy_spawn" → regular enemy spawn point
                  type "boss_spawn"  → boss spawn point
                  type "door"        → room exit trigger
                  type "potion"      → pre-placed potion pickup
                  type "gold"        → pre-placed gold pickup

Install:  pip install pytmx

Week 1:  load + render Ground/Walls, expose wall_rects
Week 3:  parse Objects layer for spawn_points
"""
import pygame

try:
    import pytmx
    _PYTMX = True
except ImportError:
    _PYTMX = False
    print("[TileMap] pytmx not found — run:  pip install pytmx")
    print("[TileMap] Falling back to a placeholder room.")


class TileMap:
    def __init__(self, tmx_path: str):
        self.path         = tmx_path
        self.wall_rects:  list = []
        self.spawn_points: list = []   # [{"type": str, "x": int, "y": int}, ...]
        self.surface:     pygame.Surface = None
        self.width  = 0   # total pixels wide
        self.height = 0   # total pixels tall

        if _PYTMX:
            self._load_tmx(tmx_path)
        else:
            self._load_placeholder()

    # ── Loading ────────────────────────────────────────────────────────────────

    def _load_tmx(self, path: str) -> None:
        try:
            tmap   = pytmx.load_pygame(path, pixelalpha=True)
            tile_w = tmap.tilewidth
            tile_h = tmap.tileheight
            self.width  = tmap.width  * tile_w
            self.height = tmap.height * tile_h

            self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

            for layer in tmap.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid in layer:
                        tile = tmap.get_tile_image_by_gid(gid)
                        if tile:
                            self.surface.blit(tile, (x * tile_w, y * tile_h))
                        if layer.name == "Walls" and gid:
                            self.wall_rects.append(
                                pygame.Rect(x * tile_w, y * tile_h, tile_w, tile_h)
                            )
                elif isinstance(layer, pytmx.TiledObjectGroup):
                    if layer.name == "Objects":
                        for obj in layer:
                            self.spawn_points.append({
                                "type": obj.type or obj.name,
                                "x":   int(obj.x),
                                "y":   int(obj.y),
                            })
        except Exception as e:
            print(f"[TileMap] Failed to load {path}: {e}")
            self._load_placeholder()

    def _load_placeholder(self) -> None:
        """
        Procedural fallback room used while real .tmx maps are being built.
        40×23 tiles at 32px each = 1280×736 — fills the window nicely.
        """
        cols, rows, tile = 40, 23, 32
        self.width  = cols * tile
        self.height = rows * tile
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((50, 50, 55))   # dark stone floor

        WALL = (90, 70, 50)
        for x in range(cols):
            for y in range(rows):
                is_border = (x == 0 or x == cols - 1 or y == 0 or y == rows - 1)
                # A few internal pillars for variety
                is_pillar = (x % 10 == 5 and y % 6 == 3 and
                             2 < x < cols - 2 and 2 < y < rows - 2)
                if is_border or is_pillar:
                    pygame.draw.rect(self.surface, WALL,
                                     (x * tile, y * tile, tile, tile))
                    self.wall_rects.append(
                        pygame.Rect(x * tile, y * tile, tile, tile))

        # Default spawn points
        self.spawn_points = [
            {"type": "enemy_spawn", "x": self.width // 2 + 200, "y": self.height // 2},
            {"type": "enemy_spawn", "x": self.width // 2 + 350, "y": self.height // 2 - 80},
        ]

    # ── Per-frame ─────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface, camera=None) -> None:
        if self.surface is None:
            return
        ox = -int(camera.offset.x) if camera else 0
        oy = -int(camera.offset.y) if camera else 0
        surface.blit(self.surface, (ox, oy))
