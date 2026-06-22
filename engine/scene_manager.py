"""
SceneManager
─────────────
Stack-based scene system.

Usage:
    manager = SceneManager(screen)
    manager.push(MainMenu(manager))        # open main menu
    manager.push(GameScene(manager))       # open game on top
    manager.pop()                          # return to menu
    manager.replace(GameOver(manager))     # swap top scene
"""
import pygame


class Scene:
    """Base class every scene inherits from."""

    def __init__(self, manager: "SceneManager"):
        self.manager = manager

    def handle_events(self, events: list) -> None:
        """Process input events."""

    def update(self, dt: float) -> None:
        """Update game state. dt is seconds since last frame."""

    def draw(self) -> None:
        """Render to self.manager.screen."""


class SceneManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self._stack: list[Scene] = []

    # ── Stack operations ──────────────────────────────────────────────────────

    def push(self, scene: Scene) -> None:
        """Push a new scene on top of the stack."""
        self._stack.append(scene)

    def pop(self) -> None:
        """Remove the top scene and return to the one below."""
        if self._stack:
            self._stack.pop()

    def replace(self, scene: Scene) -> None:
        """Swap the current scene with a new one."""
        if self._stack:
            self._stack.pop()
        self._stack.append(scene)

    @property
    def current(self):
        return self._stack[-1] if self._stack else None

    # ── Per-frame calls ───────────────────────────────────────────────────────

    def handle_events(self, events: list) -> None:
        if self.current:
            self.current.handle_events(events)

    def update(self, dt: float) -> None:
        if self.current:
            self.current.update(dt)

    def draw(self) -> None:
        if self.current:
            self.current.draw()
