"""
Camera
──────
Follows the player with smooth lerp. Clamps to room boundaries.

Usage:
    camera = Camera(room_width, room_height, WINDOW_WIDTH, WINDOW_HEIGHT)
    camera.follow(player.rect.center)    # call every frame
    camera.apply(sprite.rect)            # returns screen-space rect
"""
import pygame


class Camera:
    def __init__(self, map_width: int, map_height: int,
                 view_width: int, view_height: int,
                 lerp_speed: float = 0.1):
        self.map_width   = map_width
        self.map_height  = map_height
        self.view_width  = view_width
        self.view_height = view_height
        self.lerp_speed  = lerp_speed
        self.offset      = pygame.math.Vector2(0, 0)

    def follow(self, target_center: tuple) -> None:
        """Smoothly move the camera toward the target position."""
        target_x = target_center[0] - self.view_width  // 2
        target_y = target_center[1] - self.view_height // 2

        # Lerp toward target
        self.offset.x += (target_x - self.offset.x) * self.lerp_speed
        self.offset.y += (target_y - self.offset.y) * self.lerp_speed

        # Clamp to map bounds
        self.offset.x = max(0, min(self.offset.x, self.map_width  - self.view_width))
        self.offset.y = max(0, min(self.offset.y, self.map_height - self.view_height))

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        """Convert a world-space rect to screen-space."""
        return rect.move(-int(self.offset.x), -int(self.offset.y))

    def apply_point(self, point: tuple) -> tuple:
        """Convert a world-space point to screen-space."""
        return (
            point[0] - int(self.offset.x),
            point[1] - int(self.offset.y),
        )
