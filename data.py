SAVE_FILE = "rpg_save.json"

# ── Upgrade cost tables ───────────────────────────────────────────────────────
# Index 0 = cost to reach level 1, index 1 = level 2, index 2 = level 3
ATTACK_UPGRADE_COSTS = [75, 150, 250]

CHAMPION_UPGRADE_COSTS = {
    "vitality": [100, 200, 350, 550, 800],   # +15 max HP per tier
    "ferocity": [150, 300, 500, 750, 1100],  # +10% damage per tier
    "fortune":  [80,  160, 280, 440, 650],   # +15% gold earned per tier
}

# ── Relics ────────────────────────────────────────────────────────────────────
RELICS = {
    "Tyrant's Marrow": {
        "description": "+25 max HP permanently.",
        "bonus_hp": 25,
        "dropped_by": "Malgrim the Bone Tyrant",
    },
    "Infernal Ember": {
        "description": "Burn damage deals +2 extra per tick.",
        "burn_bonus": 2,
        "dropped_by": "Vorthax the Infernal King",
    },
}

# ── Characters ────────────────────────────────────────────────────────────────
# status_effect on an attack only triggers at upgrade level 3
# locked_attack unlocks automatically when ALL base attacks reach level 3
CHARACTER_TEMPLATES = {
    "Arthur": {
        "title": "Blade of Avalon",
        "max_hp": 130,
        "passive": {
            "name": "Valor",
            "description": "Killing an enemy restores 12 HP.",
        },
        "attacks": [
            {"name": "Lionheart Slash",   "damage": [10, 15], "cooldown": 0},
            {"name": "Iron Crest Cut",    "damage": [12, 18], "cooldown": 1},
            {"name": "Excalibur's Wrath", "damage": [18, 26], "cooldown": 2},
            {"name": "Blazing Arc",       "damage": [20, 28], "cooldown": 3, "status_effect": "burn"},
            {"name": "Fury of the Gods",  "damage": [28, 40], "cooldown": 4, "status_effect": "stun"},
        ],
        "locked_attack": {
            "name": "Legend's Blade", "damage": [40, 58], "cooldown": 5, "status_effect": "burn"
        },
    },
    "Larry": {
        "title": "King of Graves",
        "max_hp": 125,
        "passive": {
            "name": "Undying",
            "description": "Once per dungeon run, survive a fatal blow at 1 HP.",
        },
        "attacks": [
            {"name": "Bonebreaker Strike",    "damage": [10, 15], "cooldown": 0},
            {"name": "Graveburst Fist",       "damage": [12, 18], "cooldown": 1},
            {"name": "Necromantic Nightmare", "damage": [18, 26], "cooldown": 2},
            {"name": "Soul Drain",            "damage": [20, 28], "cooldown": 3, "status_effect": "bleed"},
            {"name": "King of the Undead",    "damage": [28, 40], "cooldown": 4, "status_effect": "stun"},
        ],
        "locked_attack": {
            "name": "Lich Ascension", "damage": [38, 55], "cooldown": 5, "status_effect": "bleed"
        },
    },
    "Akira": {
        "title": "Shadow Samurai",
        "max_hp": 115,
        "passive": {
            "name": "Shadow Step",
            "description": "Every 3rd consecutive attack deals double damage.",
        },
        "attacks": [
            {"name": "Shadow Slice",        "damage": [11, 16], "cooldown": 0},
            {"name": "Silent Fang",         "damage": [13, 19], "cooldown": 1, "status_effect": "bleed"},
            {"name": "Phantom Dash",        "damage": [18, 25], "cooldown": 2, "status_effect": "stun"},
            {"name": "Nightfall Execution", "damage": [21, 29], "cooldown": 3},
            {"name": "Dragon Shadow Strike","damage": [30, 42], "cooldown": 4},
        ],
        "locked_attack": {
            "name": "Void Annihilation", "damage": [42, 60], "cooldown": 5, "status_effect": "bleed"
        },
    },
    "Zara": {
        "title": "Storm Mage",
        "max_hp": 110,
        "passive": {
            "name": "Chain Lightning",
            "description": "30% chance any attack hits a second time for half damage.",
        },
        "attacks": [
            {"name": "Spark Bolt",            "damage": [10, 14], "cooldown": 0},
            {"name": "Lightning Surge",       "damage": [13, 19], "cooldown": 1},
            {"name": "Thunderstorm",          "damage": [19, 26], "cooldown": 2, "status_effect": "stun"},
            {"name": "Skybreaker",            "damage": [22, 30], "cooldown": 3},
            {"name": "Wrath of the Storm God","damage": [31, 44], "cooldown": 4, "status_effect": "burn"},
        ],
        "locked_attack": {
            "name": "Tempest Judgement", "damage": [44, 62], "cooldown": 5, "status_effect": "stun"
        },
    },
    "Drakon": {
        "title": "Fire Dragon",
        "max_hp": 145,
        "passive": {
            "name": "Infernal Rage",
            "description": "Below 30% HP, all damage increased by 50%.",
        },
        "attacks": [
            {"name": "Flame Bite",           "damage": [11, 16], "cooldown": 0},
            {"name": "Inferno Claw",         "damage": [14, 20], "cooldown": 1, "status_effect": "burn"},
            {"name": "Blazing Roar",         "damage": [20, 28], "cooldown": 2},
            {"name": "Molten Fury",          "damage": [24, 33], "cooldown": 3},
            {"name": "Apocalypse Firestorm", "damage": [34, 47], "cooldown": 4, "status_effect": "burn"},
        ],
        "locked_attack": {
            "name": "Ragnarok Breath", "damage": [48, 68], "cooldown": 5, "status_effect": "burn"
        },
    },
    "Orion": {
        "title": "Cosmic Archer",
        "max_hp": 118,
        "passive": {
            "name": "Precision",
            "description": "25% chance each attack rolls maximum possible damage.",
        },
        "attacks": [
            {"name": "Star Arrow",       "damage": [10, 15], "cooldown": 0},
            {"name": "Nebula Shot",      "damage": [13, 19], "cooldown": 1},
            {"name": "Comet Barrage",    "damage": [18, 25], "cooldown": 2, "status_effect": "bleed"},
            {"name": "Galactic Pierce",  "damage": [21, 29], "cooldown": 3},
            {"name": "Supernova Strike", "damage": [30, 43], "cooldown": 4, "status_effect": "stun"},
        ],
        "locked_attack": {
            "name": "Big Bang Arrow", "damage": [46, 65], "cooldown": 5, "status_effect": "bleed"
        },
    },
}

# ── Enemies ───────────────────────────────────────────────────────────────────
REGULAR_ENEMIES = [
    {
        "name": "Goblin Marauder",
        "max_hp": 70,
        "attacks": [
            {"name": "Rusty Stab",  "damage": [7, 11], "cooldown": 0},
            {"name": "Wild Swing",  "damage": [8, 13], "cooldown": 1},
        ],
        "reward_gold": 20,
        "reward_potions": 1,
    },
    {
        "name": "Skeleton Knight",
        "max_hp": 85,
        "attacks": [
            {"name": "Bone Slash",  "damage": [8, 13], "cooldown": 0},
            {"name": "Shield Bash", "damage": [9, 14], "cooldown": 1},
        ],
        "reward_gold": 25,
        "reward_potions": 1,
    },
    {
        "name": "Shadow Beast",
        "max_hp": 95,
        "attacks": [
            {"name": "Dark Claw",   "damage": [10, 15], "cooldown": 0},
            {"name": "Night Pounce","damage": [11, 16], "cooldown": 1},
        ],
        "reward_gold": 30,
        "reward_potions": 1,
    },
    {
        "name": "Flame Wraith",
        "max_hp": 100,
        "attacks": [
            {"name": "Ember Touch",    "damage": [11, 16], "cooldown": 0},
            {"name": "Burning Scream", "damage": [12, 17], "cooldown": 1},
        ],
        "reward_gold": 35,
        "reward_potions": 1,
    },
]

BOSSES = [
    {
        "name": "Malgrim the Bone Tyrant",
        "max_hp": 180,
        "attacks": [
            {"name": "Tyrant Cleave", "damage": [16, 24], "cooldown": 1},
            {"name": "Skull Quake",   "damage": [18, 26], "cooldown": 2},
            {"name": "Legion Call",   "damage": [20, 29], "cooldown": 3},
        ],
        "reward_gold": 80,
        "reward_potions": 2,
        "relic_drop": "Tyrant's Marrow",
    },
    {
        "name": "Vorthax the Infernal King",
        "max_hp": 220,
        "attacks": [
            {"name": "Hellfire Slam", "damage": [18, 27], "cooldown": 1},
            {"name": "Inferno Burst", "damage": [20, 30], "cooldown": 2},
            {"name": "Doomflame",     "damage": [23, 34], "cooldown": 3},
        ],
        "reward_gold": 120,
        "reward_potions": 3,
        "relic_drop": "Infernal Ember",
    },
]
