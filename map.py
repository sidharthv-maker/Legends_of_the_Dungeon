# map.py  –  walkable floor ellipse definitions
# Screen: 1280 x 720
#
# Each entry is a pygame.Rect tuple (left, top, width, height) that is passed
# to pygame.draw.ellipse() to paint the walkable floor area.
# The mask is built from that surface: inside the ellipse = walkable.
#
# Right edge is intentionally 1280 (full screen width) so the door on the
# right wall is always reachable.

# ── Default ellipse  (fits all 18 maps) ──────────────────────────────────────
#   left=80   → blocks left wall (~x 80-110 is stone in all maps)
#   top=368   → blocks top background / hanging stalactites
#   width=1200 → right edge at x=1280, door fully reachable
#   height=282 → bottom edge at y=650, covers full cobblestone floor
DEFAULT_ELLIPSE = (60, 345, 1220, 320)

# ── Per-map overrides ─────────────────────────────────────────────────────────
# Maps whose floor shape differs enough to need a custom ellipse.
# Add entries as needed; format: map_number: (left, top, width, height)
MAP_ELLIPSE_OVERRIDES = {
    # Example:  5: (90, 375, 1190, 270),
}

def get_ellipse(map_number):
    """Return the walkable ellipse rect for map_number (1-based, 1..18)."""
    return MAP_ELLIPSE_OVERRIDES.get(map_number, DEFAULT_ELLIPSE)
