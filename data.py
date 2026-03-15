SAVE_FILE = "rpg_save.json"

CHARACTER_TEMPLATES = {
    "Arthur": {
        "title": "Blade of Avalon",
        "max_hp": 130,
        "attacks": [
            {"name": "Lionheart Slash", "damage": [10, 15], "cooldown": 0},
            {"name": "Iron Crest Cut", "damage": [12, 18], "cooldown": 1},
            {"name": "Excalibur's Wrath", "damage": [18, 26], "cooldown": 2},
            {"name": "Blazing Arc", "damage": [20, 28], "cooldown": 3},
            {"name": "Fury of the Gods", "damage": [28, 40], "cooldown": 4},
        ],
    },
    "Larry": {
        "title": "King of Graves",
        "max_hp": 125,
        "attacks": [
            {"name": "Bonebreaker Strike", "damage": [10, 15], "cooldown": 0},
            {"name": "Graveburst Fist", "damage": [12, 18], "cooldown": 1},
            {"name": "Necromantic Nightmare", "damage": [18, 26], "cooldown": 2},
            {"name": "Soul Drain", "damage": [20, 28], "cooldown": 3},
            {"name": "King of the Undead", "damage": [28, 40], "cooldown": 4},
        ],
    },
    "Akira": {
        "title": "Shadow Samurai",
        "max_hp": 115,
        "attacks": [
            {"name": "Shadow Slice", "damage": [11, 16], "cooldown": 0},
            {"name": "Silent Fang", "damage": [13, 19], "cooldown": 1},
            {"name": "Phantom Dash", "damage": [18, 25], "cooldown": 2},
            {"name": "Nightfall Execution", "damage": [21, 29], "cooldown": 3},
            {"name": "Dragon Shadow Strike", "damage": [30, 42], "cooldown": 4},
        ],
    },
    "Zara": {
        "title": "Storm Mage",
        "max_hp": 110,
        "attacks": [
            {"name": "Spark Bolt", "damage": [10, 14], "cooldown": 0},
            {"name": "Lightning Surge", "damage": [13, 19], "cooldown": 1},
            {"name": "Thunderstorm", "damage": [19, 26], "cooldown": 2},
            {"name": "Skybreaker", "damage": [22, 30], "cooldown": 3},
            {"name": "Wrath of the Storm God", "damage": [31, 44], "cooldown": 4},
        ],
    },
    "Drakon": {
        "title": "Fire Dragon",
        "max_hp": 145,
        "attacks": [
            {"name": "Flame Bite", "damage": [11, 16], "cooldown": 0},
            {"name": "Inferno Claw", "damage": [14, 20], "cooldown": 1},
            {"name": "Blazing Roar", "damage": [20, 28], "cooldown": 2},
            {"name": "Molten Fury", "damage": [24, 33], "cooldown": 3},
            {"name": "Apocalypse Firestorm", "damage": [34, 47], "cooldown": 4},
        ],
    },
    "Orion": {
        "title": "Cosmic Archer",
        "max_hp": 118,
        "attacks": [
            {"name": "Star Arrow", "damage": [10, 15], "cooldown": 0},
            {"name": "Nebula Shot", "damage": [13, 19], "cooldown": 1},
            {"name": "Comet Barrage", "damage": [18, 25], "cooldown": 2},
            {"name": "Galactic Pierce", "damage": [21, 29], "cooldown": 3},
            {"name": "Supernova Strike", "damage": [30, 43], "cooldown": 4},
        ],
    },
}

REGULAR_ENEMIES = [
    {
        "name": "Goblin Marauder",
        "max_hp": 70,
        "attacks": [
            {"name": "Rusty Stab", "damage": [7, 11], "cooldown": 0},
            {"name": "Wild Swing", "damage": [8, 13], "cooldown": 1},
        ],
        "reward_gold": 20,
        "reward_potions": 1,
    },
    {
        "name": "Skeleton Knight",
        "max_hp": 85,
        "attacks": [
            {"name": "Bone Slash", "damage": [8, 13], "cooldown": 0},
            {"name": "Shield Bash", "damage": [9, 14], "cooldown": 1},
        ],
        "reward_gold": 25,
        "reward_potions": 1,
    },
    {
        "name": "Shadow Beast",
        "max_hp": 95,
        "attacks": [
            {"name": "Dark Claw", "damage": [10, 15], "cooldown": 0},
            {"name": "Night Pounce", "damage": [11, 16], "cooldown": 1},
        ],
        "reward_gold": 30,
        "reward_potions": 1,
    },
    {
        "name": "Flame Wraith",
        "max_hp": 100,
        "attacks": [
            {"name": "Ember Touch", "damage": [11, 16], "cooldown": 0},
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
            {"name": "Skull Quake", "damage": [18, 26], "cooldown": 2},
            {"name": "Legion Call", "damage": [20, 29], "cooldown": 3},
        ],
        "reward_gold": 80,
        "reward_potions": 2,
    },
    {
        "name": "Vorthax the Infernal King",
        "max_hp": 220,
        "attacks": [
            {"name": "Hellfire Slam", "damage": [18, 27], "cooldown": 1},
            {"name": "Inferno Burst", "damage": [20, 30], "cooldown": 2},
            {"name": "Doomflame", "damage": [23, 34], "cooldown": 3},
        ],
        "reward_gold": 120,
        "reward_potions": 3,
    },
]
