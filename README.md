# Legends of the Dungeon

A modular console RPG written in Python.

This version restructures the original single-file game into smaller, easier-to-maintain modules. It includes:

- multiple playable heroes
- dungeon floors
- regular enemies and boss fights
- attack cooldowns
- potion-based healing
- auto-save / manual save support
- JSON save file loading and deletion
- HP bars after each round

## Project Structure

```text
legends_of_the_dungeon/
├── main.py           # Entry point
├── data.py           # Static game data: heroes, enemies, bosses, save filename
├── models.py         # Fighter, Player, Enemy classes
├── utils.py          # UI helpers and input utilities
├── save_system.py    # Save, load, delete logic
├── game_logic.py     # Character selection, battles, dungeon flow, main menu
└── README.md         # Documentation
```

## Requirements

- Python 3.10+ recommended
- No external libraries required

## How to Run

Open a terminal in the project folder and run:

```bash
python main.py
```

On some systems you may need:

```bash
python3 main.py
```

## Gameplay Overview

### Main Menu

When the game starts, you can:

1. Start a new game
2. Load an existing save
3. Delete the save file
4. Quit

### Battle System

Each turn, the player can:

1. Attack
2. Use Potion
3. Save Game
4. View Hero Info

Attacks have:

- a damage range
- a cooldown value

Once used, an attack becomes unavailable until its cooldown expires.

### Dungeon Progression

- The player starts on floor 1.
- Every floor spawns an enemy.
- Every 3rd floor is a boss floor.
- Enemies scale with dungeon depth.
- After each win, the player gets rewards and a small HP recovery.
- The game auto-saves after each cleared floor.

## Save System

The game stores progress in:

```text
rpg_save.json
```

The save file contains:

- hero name and title
- current HP
- attack cooldown timers
- gold
- potions
- current floor
- wins
- bosses defeated

## Why This Modular Version Is Better

Compared to the original single-file version, this structure improves:

### 1. Readability

Game data, classes, save logic, and gameplay are separated into their own files.

### 2. Maintainability

You can update one part of the game without digging through a huge script.

Examples:

- add new heroes in `data.py`
- change combat rules in `game_logic.py`
- improve save behavior in `save_system.py`

### 3. Reusability

The `Player`, `Enemy`, and `Fighter` classes can be reused for future features like:

- equipment
- level-ups
- status effects
- shops
- multiplayer simulation

### 4. Easier Expansion

This structure is much better for adding future systems such as:

- inventory
- armor and weapons
- mana / magic
- skills tree
- critical hits
- elemental damage
- different dungeon biomes

## Known Improvement Made During Modularization

The original code had this line inside `dungeon_mode()`:

```python
choice = ask_int("\nChoose: ", 1, 3)
```

But only two options were printed. That has been corrected to:

```python
choice = ask_int("\nChoose: ", 1, 2)
```

## How to Add a New Character

In `data.py`, add another entry inside `CHARACTER_TEMPLATES`:

```python
"Nyra": {
    "title": "Frost Witch",
    "max_hp": 112,
    "attacks": [
        {"name": "Ice Shard", "damage": [10, 14], "cooldown": 0},
        {"name": "Frost Bind", "damage": [12, 18], "cooldown": 1},
        {"name": "Glacier Spear", "damage": [18, 26], "cooldown": 2},
        {"name": "Winter Collapse", "damage": [22, 30], "cooldown": 3},
        {"name": "Absolute Zero", "damage": [30, 44], "cooldown": 4},
    ],
}
```

The character will automatically appear in the character selection menu.

## How to Add a New Regular Enemy

In `data.py`, append a dictionary to `REGULAR_ENEMIES` with:

- `name`
- `max_hp`
- `attacks`
- `reward_gold`
- `reward_potions`

## Future Refactor Suggestions

If you want to take this one step further, the next good upgrades would be:

1. create a dedicated `BattleEngine` class
2. create a `Game` class to hold global state
3. move all display text into a separate UI layer
4. split enemy generation into a separate `enemy_factory.py`
5. add tests for save/load and cooldown logic

## License

Use and modify freely for personal learning.
