"""
InputHandler
────────────
Maps raw keyboard input to named game actions.
Add or rebind actions here — nothing else in the codebase needs to change.

Actions:
    move_up, move_down, move_left, move_right
    attack, use_potion, pause, confirm, cancel
"""
import pygame

# Default keyboard bindings  (action → pygame key constant)
DEFAULT_BINDINGS: dict = {
    "move_up":    pygame.K_w,
    "move_down":  pygame.K_s,
    "move_left":  pygame.K_a,
    "move_right": pygame.K_d,
    "attack":     pygame.K_j,
    "use_potion": pygame.K_k,
    "pause":      pygame.K_ESCAPE,
    "confirm":    pygame.K_RETURN,
    "cancel":     pygame.K_BACKSPACE,
}


class InputHandler:
    def __init__(self, bindings: dict = None):
        self.bindings        = bindings or DEFAULT_BINDINGS
        self._held:          set = set()
        self._just_pressed:  set = set()
        self._just_released: set = set()

    def update(self, events: list) -> None:
        """Call once per frame with the event list from pygame.event.get()."""
        self._just_pressed.clear()
        self._just_released.clear()

        pressed_keys = pygame.key.get_pressed()

        for action, key in self.bindings.items():
            if pressed_keys[key]:
                if action not in self._held:
                    self._just_pressed.add(action)
                self._held.add(action)
            else:
                if action in self._held:
                    self._just_released.add(action)
                self._held.discard(action)

    # ── Query helpers ─────────────────────────────────────────────────────────

    def held(self, action: str) -> bool:
        """True while the key is held down."""
        return action in self._held

    def just_pressed(self, action: str) -> bool:
        """True on the first frame the key is pressed."""
        return action in self._just_pressed

    def just_released(self, action: str) -> bool:
        """True on the first frame the key is released."""
        return action in self._just_released

    def movement_vector(self) -> pygame.math.Vector2:
        """Returns a normalised direction vector from WASD input."""
        vec = pygame.math.Vector2(0, 0)
        if self.held("move_up"):    vec.y -= 1
        if self.held("move_down"):  vec.y += 1
        if self.held("move_left"):  vec.x -= 1
        if self.held("move_right"): vec.x += 1
        if vec.length() > 0:
            vec.normalize_ip()
        return vec
