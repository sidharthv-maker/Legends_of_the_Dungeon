SAVE_FILE = "rpg_save.json"

# ── Speed classes ─────────────────────────────────────────────────────────────
PLAYER_SPEED_MAP = {
    "slow":      200,
    "medium":    240,
    "fast":      270,
    "very fast": 300,
}

ENEMY_SPEED_MAP = {
    "very slow": 50,
    "slow":      75,
    "medium":    100,
    "fast":      130,
    "very fast": 150,
}

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
    "Plague Crown": {
        "description": "Bleed applies one extra stack on hit.",
        "bleed_bonus_stacks": 1,
        "dropped_by": "Seraphine the Plague Queen",
    },
    "Titan's Core": {
        "description": "+40 max HP permanently.",
        "bonus_hp": 40,
        "dropped_by": "Korgath the Stone Titan",
    },
    "Void Fragment": {
        "description": "10% chance to dodge any incoming hit entirely.",
        "dodge_chance": 0.10,
        "dropped_by": "Nyx the Void Empress",
    },
    "Judge's Seal": {
        "description": "All damage dealt increased by 10% permanently.",
        "damage_bonus": 0.10,
        "dropped_by": "Azrael the Final Judge",
    },
}

# ── Characters ────────────────────────────────────────────────────────────────
# status_effect on an attack only triggers at upgrade level 3
# locked_attack unlocks automatically when ALL base attacks reach level 3
CHARACTER_TEMPLATES = {
    "Arthur": {
        "title": "Blade of Avalon",
        "max_hp": 130,
        "speed": "medium",
        "scale": 1.25,
        "sprite_folder": "arthur",
        "sprites": {
            "idle_left":     ["arthur_idle_left_1.png",   "arthur_idle_left_2.png"],
            "idle_right":    ["arthur_idle_right_1.png",  "arthur_idle_right_2.png"],
            "idle_front":    ["arthur_front.png"],
            "idle_back":     ["arthur_back.png"],
            "walk_left":     ["arthur_walk_left_1.png",   "arthur_walk_left_2.png",   "arthur_walk_left_3.png"],
            "walk_right":    ["arthur_walk_right_1.png",  "arthur_walk_right_2.png",  "arthur_walk_right_3.png"],
            "attack_right":  ["arthur_basic_left_1.png",  "arthur_basic_left_2.png"],
            "attack_left":   ["arthur_basic_right_1.png", "arthur_basic_right_2.png"],
            "special_right": ["arthur_special_left_1.png",  "arthur_special_left_2.png","arthur_special_left_2.png","arthur_special_left_2.png",  "arthur_special_left_3.png"],
            "special_left":  ["arthur_special_right_1.png", "arthur_special_right_2.png","arthur_special_right_2.png","arthur_special_right_2.png", "arthur_special_right_3.png"],
        },
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
        "speed": "slow",
        "scale": 4.0,
        "sprite_folder": "larry",
        "sprites": {
            "idle_left":     ["01_main_left.png", "01_main_left.png"],              # 05/06 broken – placeholder
            "idle_right":    ["07_idle_right_01.png", "08_idle_right_02.png"],
            "idle_front":    ["02_main_front.png"],
            "idle_back":     ["04_main_back.png"],
            "walk_left":     ["07_walk_left_01.png", "08_walk_left_02.png", "09_walk_left_03.png"],
            "walk_right":    ["07_idle_right_01.png", "08_idle_right_02.png"],      # no walk_right sprites yet
            "attack_right":  ["10_basic_attack_right_01.png", "11_basic_attack_right_02.png"],
            "attack_left":   ["10_basic_attack_right_01.png", "11_basic_attack_right_02.png"],  # no attack_left yet
            "special_right": ["12_special_attack_left_01.png", "12_special_attack_left_01.png", "12_special_attack_left_01.png", "12_special_attack_left_01.png"],  # 13/14 are wrong (dragon)
            "special_left":  ["12_special_attack_left_01.png", "12_special_attack_left_01.png", "12_special_attack_left_01.png", "12_special_attack_left_01.png"],
        },
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
        "speed": "fast",
        "scale": 1.25,
        "sprite_folder": "akira/akira_sprites_transparent_hires",
        "sprites": {
            "idle_left":     ["akira_idle_left_f1.png",  "akira_idle_left_f2.png"],
            "idle_right":    ["akira_idle_right_f1.png", "akira_idle_right_f2.png"],
            "idle_front":    ["akira_main_front.png"],
            "idle_back":     ["akira_main_back.png"],
            "walk_left":     ["akira_walk_left_f1.png",  "akira_walk_left_f2.png",  "akira_walk_left_f3.png"],
            "walk_right":    ["akira_walk_right_f1.png", "akira_walk_right_f2.png", "akira_walk_right_f3.png"],
            "attack_right":  ["akira_basic_left_f1.png",  "akira_basic_left_f2.png"],
            "attack_left":   ["akira_basic_right_f1.png", "akira_basic_right_f2.png"],
            "special_right": ["akira_special_left_f1.png",  "akira_special_left_f2.png", "akira_special_left_f2.png", "akira_special_left_f3.png"],
            "special_left":  ["akira_special_right_f1.png", "akira_special_right_f2.png", "akira_special_right_f2.png","akira_special_right_f3.png"],
        },
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
        "speed": "medium",
        "scale": 1.25,
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
        "sprite_folder": "zara",
        "sprites": {
            "idle_left":     ["idle_left_1.png",  "idle_left_2.png"],
            "idle_right":    ["idle_right_1.png", "idle_right_2.png"],
            "idle_front":    ["main_front.png"],
            "idle_back":     ["main_back.png"],
            "walk_left":     ["walk_left_1.png",  "walk_left_2.png",  "walk_left_3.png"],
            "walk_right":    ["walk_right_1.png", "walk_right_2.png", "walk_right_3.png"],
            "attack_right":  ["basic_attack_left_1.png",  "basic_attack_left_2.png"],
            "attack_left":   ["basic_attack_right_1.png", "basic_attack_right_2.png"],
            "special_right": ["special_attack_left_1.png", "special_attack_left_2.png","special_attack_left_2.png","special_attack_left_2.png", "special_attack_left_3_effect.png"],
            "special_left":  ["special_attack_right_3.png", "special_attack_right_2.png","special_attack_right_2.png","special_attack_right_2.png", "special_attack_right_3.png"],
        },
    },
    "Drakon": {
        "title": "Fire Dragon",
        "max_hp": 145,
        "speed": "medium",
        "scale": 1.25,
        "sprite_folder": "drakon",
        "sprites": {
            "idle_left":     ["idle_left_1.png",  "idle_left_2.png"],
            "idle_right":    ["idle_right_1.png", "idle_right_2.png"],
            "idle_front":    ["main_front.png"],
            "idle_back":     ["main_back.png"],
            "walk_left":     ["walk_left_1.png",  "walk_left_2.png",  "walk_left_3.png"],
            "walk_right":    ["walk_right_1.png", "walk_right_2.png", "walk_right_3.png"],
            "attack_right":  ["basic_attack_left_1.png",  "basic_attack_left_2.png"],
            "attack_left":   ["basic_attack_right_1.png", "basic_attack_right_2.png"],
            "special_right": ["special_attack_left_1.png", "special_attack_left_2.png","special_attack_left_2.png","special_attack_left_2.png"],
            "special_left":  ["special_attack_right_3.png", "special_attack_right_2.png","special_attack_right_2.png","special_attack_right_2.png"],
        },
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
        "speed": "fast",
        "scale": 1.25,
        "sprite_folder": "orion",
        "sprites": {
            "idle_left":     ["05_idle_left_frame1.png",  "06_idle_left_frame2.png"],
            "idle_right":    ["07_idle_right_frame1.png", "08_idle_right_frame2.png"],
            "idle_front":    ["02_main_reference_front.png"],
            "idle_back":     ["04_main_reference_back.png"],
            "walk_left":     ["09_walk_left_frame1.png",  "10_walk_left_frame2.png",  "11_walk_left_frame3.png"],
            "walk_right":    ["12_walk_right_frame1.png", "13_walk_right_frame2.png", "14_walk_right_frame3.png"],
            "attack_right":  ["15_basic_attack_left_frame1.png",  "16_basic_attack_left_frame2.png"],
            "attack_left":   ["17_basic_attack_right_frame1_projectile.png", "18_basic_attack_right_frame2.png"],
            "special_right": ["19_special_attack_left_frame1.png",  "20_special_attack_left_frame2_charge.png",  "21_special_attack_left_frame3_projectile.png"],
            "special_left":  ["22_special_attack_right_frame1.png", "23_special_attack_right_frame2_charge.png", "24_special_attack_right_frame3_projectile.png"],
        },
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
    # ── Tier 1 (early rooms) ──────────────────────────────────────────────────
    {
        "name": "Goblin Marauder",
        "max_hp": 70,
        "speed": "fast",
        "attacks": [
            {"name": "Rusty Stab",  "damage": [7, 11], "cooldown": 0},
            {"name": "Wild Swing",  "damage": [8, 13], "cooldown": 1},
        ],
        "reward_gold": 20,
        "reward_potions": 1,
        "sprite_folder": "tier1/goblin",
        "sprites": {
            "idle_left":    ["05_goblin_marauder_idle_left_01.png",  "06_goblin_marauder_idle_left_02.png"],
            "idle_right":   ["07_goblin_marauder_idle_right_01.png", "08_goblin_marauder_idle_right_02.png"],
            "walk_left":    ["09_goblin_marauder_walk_left_01.png",  "10_goblin_marauder_walk_left_02.png",  "11_goblin_marauder_walk_left_03.png"],
            "walk_right":   ["12_goblin_marauder_walk_right_01.png", "13_goblin_marauder_walk_right_02.png", "14_goblin_marauder_walk_right_03.png"],
            "attack_left":  ["15_goblin_marauder_rusty_stab_left_01.png",  "16_goblin_marauder_rusty_stab_left_02.png"],
            "attack_right": ["17_goblin_marauder_rusty_stab_right_01.png", "18_goblin_marauder_rusty_stab_right_02.png"],
            "death":        ["25_goblin_marauder_death_01.png", "26_goblin_marauder_death_02.png", "27_goblin_marauder_death_03.png", "28_goblin_marauder_death_04.png"],
        },
    },
    {
        "name": "Plague Rat",
        "max_hp": 55,
        "speed": "very fast",
        "attacks": [
            {"name": "Gnaw", "damage": [5,  9],  "cooldown": 0},
            {"name": "Infected Bite", "damage": [6, 10], "cooldown": 1, "status_effect": "bleed"},
        ],
        "reward_gold": 18,
        "reward_potions": 1,
        "sprite_folder": "tier1/rat",
        "sprites": {
            "idle_left":    ["05_plague_rat_idle_left_01.png",  "06_plague_rat_idle_left_02.png"],
            "idle_right":   ["07_plague_rat_idle_right_01.png", "08_plague_rat_idle_right_02.png"],
            "walk_left":    ["09_plague_rat_walk_left_01.png",  "10_plague_rat_walk_left_02.png",  "11_plague_rat_walk_left_03.png"],
            "walk_right":   ["12_plague_rat_walk_right_01.png", "13_plague_rat_walk_right_02.png", "14_plague_rat_walk_right_03.png"],
            "attack_left":  ["15_plague_rat_gnaw_left_01.png",  "16_plague_rat_gnaw_left_02.png"],
            "attack_right": ["17_plague_rat_gnaw_right_01.png", "18_plague_rat_gnaw_right_02.png"],
            "death":        ["27_plague_rat_death_01.png", "28_plague_rat_death_02.png", "29_plague_rat_death_03.png", "30_plague_rat_death_04.png"],
        },
    },
    {
        "name": "Skeleton Knight",
        "max_hp": 85,
        "speed": "medium",
        "attacks": [
            {"name": "Bone Slash",  "damage": [8, 13], "cooldown": 0},
            {"name": "Shield Bash", "damage": [9, 14], "cooldown": 1, "status_effect": "stun"},
        ],
        "reward_gold": 25,
        "reward_potions": 1,
        "sprite_folder": "tier1/skeleton_knight",
        "sprites": {
            "idle_left":    ["05_skeleton_knight_idle_left_01.png",  "06_skeleton_knight_idle_left_02.png"],
            "idle_right":   ["07_skeleton_knight_idle_right_01.png", "08_skeleton_knight_idle_right_02.png"],
            "walk_left":    ["09_skeleton_knight_walk_left_01.png",  "10_skeleton_knight_walk_left_02.png",  "11_skeleton_knight_walk_left_03.png"],
            "walk_right":   ["12_skeleton_knight_walk_right_01.png", "13_skeleton_knight_walk_right_02.png", "14_skeleton_knight_walk_right_03.png"],
            "attack_left":  ["15_skeleton_knight_bone_slash_left_01.png",  "16_skeleton_knight_bone_slash_left_02.png"],
            "attack_right": ["17_skeleton_knight_bone_slash_right_01.png", "18_skeleton_knight_bone_slash_right_02.png"],
            "death":        ["25_skeleton_knight_death_01.png", "26_skeleton_knight_death_02.png", "27_skeleton_knight_death_03.png", "28_skeleton_knight_death_04.png"],
        },
    },
    {
        "name": "Venom Spider",
        "max_hp": 65,
        "speed": "fast",
        "attacks": [
            {"name": "Venomous Bite",  "damage": [6, 10], "cooldown": 0, "status_effect": "bleed"},
            {"name": "Web Snare",      "damage": [5,  8], "cooldown": 1, "status_effect": "stun"},
        ],
        "reward_gold": 22,
        "reward_potions": 1,
        "sprite_folder": "tier1/spider",
        "sprites": {
            "idle_left":    ["05_venom_spider_idle_left_01.png",  "06_venom_spider_idle_left_02.png"],
            "idle_right":   ["07_venom_spider_idle_right_01.png", "08_venom_spider_idle_right_02.png"],
            "walk_left":    ["09_venom_spider_walk_left_01.png",  "10_venom_spider_walk_left_02.png",  "11_venom_spider_walk_left_03.png"],
            "walk_right":   ["12_venom_spider_walk_right_01.png", "13_venom_spider_walk_right_02.png", "14_venom_spider_walk_right_03.png"],
            "attack_left":  ["15_venom_spider_venomous_bite_left_01.png",  "16_venom_spider_venomous_bite_left_02.png"],
            "attack_right": ["17_venom_spider_venomous_bite_right_01.png", "18_venom_spider_venomous_bite_right_02.png"],
            "death":        ["27_venom_spider_death_01.png", "28_venom_spider_death_02.png", "29_venom_spider_death_03.png", "30_venom_spider_death_04.png"],
        },
    },
    # ── Tier 2 (mid rooms) ────────────────────────────────────────────────────
    {
        "name": "Shadow Beast",
        "max_hp": 95,
        "speed": "fast",
        "attacks": [
            {"name": "Dark Claw",    "damage": [10, 15], "cooldown": 0},
            {"name": "Night Pounce", "damage": [11, 16], "cooldown": 1},
        ],
        "reward_gold": 30,
        "reward_potions": 1,
    },
    {
        "name": "Flame Wraith",
        "max_hp": 100,
        "speed": "medium",
        "attacks": [
            {"name": "Ember Touch",    "damage": [11, 16], "cooldown": 0, "status_effect": "burn"},
            {"name": "Burning Scream", "damage": [12, 17], "cooldown": 1},
        ],
       "reward_gold": 35,
        "reward_potions": 1,
    },
    {
        "name": "Frost Revenant",
        "max_hp": 90,
        "speed": "slow",
        "attacks": [
            {"name": "Glacial Strike", "damage": [10, 15], "cooldown": 0},
            {"name": "Ice Shatter",    "damage": [12, 18], "cooldown": 1, "status_effect": "stun"},
        ],
        "reward_gold": 32,
        "reward_potions": 1,
    },
    {
        "name": "Blood Cultist",
        "max_hp": 80,
        "speed": "medium",
        "attacks": [
            {"name": "Blood Ritual",  "damage": [9,  14], "cooldown": 0, "status_effect": "bleed"},
            {"name": "Sacrificial Cut","damage": [11, 16], "cooldown": 1, "status_effect": "bleed"},
        ],
        "reward_gold": 38,
        "reward_potions": 1,
    },
    # ── Tier 3 (deep rooms) ───────────────────────────────────────────────────
    {
        "name": "Thunder Drake",
        "max_hp": 115,
        "speed": "fast",
        "attacks": [
            {"name": "Storm Bite",     "damage": [13, 19], "cooldown": 0},
            {"name": "Lightning Tail", "damage": [14, 21], "cooldown": 1, "status_effect": "burn"},
        ],
        "reward_gold": 45,
        "reward_potions": 1,
    },
    {
        "name": "Stone Golem",
        "max_hp": 150,
        "speed": "very slow",
        "attacks": [
            {"name": "Boulder Fist",  "damage": [15, 22], "cooldown": 0, "status_effect": "stun"},
            {"name": "Tremor Stomp",  "damage": [16, 24], "cooldown": 2},
        ],
        "reward_gold": 50,
        "reward_potions": 2,
    },
    {
        "name": "Iron Executioner",
        "max_hp": 125,
        "speed": "slow",
        "attacks": [
            {"name": "Guillotine Drop",  "damage": [16, 23], "cooldown": 0},
            {"name": "Headsman's Blow",  "damage": [18, 26], "cooldown": 2, "status_effect": "bleed"},
        ],
        "reward_gold": 55,
        "reward_potions": 2,
    },
    {
        "name": "Void Stalker",
        "max_hp": 110,
        "speed": "very fast",
        "attacks": [
            {"name": "Phase Slash",   "damage": [14, 20], "cooldown": 0},
            {"name": "Void Rupture",  "damage": [17, 25], "cooldown": 1, "status_effect": "bleed"},
            {"name": "Null Erasure",  "damage": [20, 28], "cooldown": 3, "status_effect": "stun"},
        ],
        "reward_gold": 60,
        "reward_potions": 2,
    },
]

BOSSES = [
    {
        "name": "Malgrim the Bone Tyrant",
        "max_hp": 180,
        "speed": "slow",
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
        "speed": "medium",
        "attacks": [
            {"name": "Hellfire Slam", "damage": [18, 27], "cooldown": 1},
            {"name": "Inferno Burst", "damage": [20, 30], "cooldown": 2, "status_effect": "burn"},
            {"name": "Doomflame",     "damage": [23, 34], "cooldown": 3, "status_effect": "burn"},
        ],
        "reward_gold": 120,
        "reward_potions": 3,
        "relic_drop": "Infernal Ember",
    },
    {
        "name": "Seraphine the Plague Queen",
        "max_hp": 260,
        "speed": "medium",
        "attacks": [
            {"name": "Pestilent Grasp",  "damage": [17, 25], "cooldown": 1, "status_effect": "bleed"},
            {"name": "Swarm Release",    "damage": [19, 28], "cooldown": 2, "status_effect": "bleed"},
            {"name": "Epidemic Surge",   "damage": [24, 35], "cooldown": 3, "status_effect": "bleed"},
        ],
        "reward_gold": 160,
        "reward_potions": 3,
        "relic_drop": "Plague Crown",
    },
    {
        "name": "Korgath the Stone Titan",
        "max_hp": 320,
        "speed": "very slow",
        "attacks": [
            {"name": "Mountain Slam",   "damage": [20, 30], "cooldown": 1, "status_effect": "stun"},
            {"name": "Rockfall Crush",  "damage": [22, 33], "cooldown": 2},
            {"name": "Titan's Wrath",   "damage": [28, 40], "cooldown": 3, "status_effect": "stun"},
        ],
        "reward_gold": 200,
        "reward_potions": 3,
        "relic_drop": "Titan's Core",
    },
    {
        "name": "Nyx the Void Empress",
        "max_hp": 370,
        "speed": "fast",
        "attacks": [
            {"name": "Shadow Lance",    "damage": [22, 32], "cooldown": 1, "status_effect": "bleed"},
            {"name": "Void Collapse",   "damage": [25, 37], "cooldown": 2, "status_effect": "stun"},
            {"name": "Empress's Curse", "damage": [30, 44], "cooldown": 3, "status_effect": "bleed"},
            {"name": "Eternal Darkness","damage": [35, 50], "cooldown": 4},
        ],
        "reward_gold": 260,
        "reward_potions": 4,
        "relic_drop": "Void Fragment",
    },
    {
        "name": "Azrael the Final Judge",
        "max_hp": 500,
        "speed": "medium",
        "attacks": [
            {"name": "Divine Verdict",   "damage": [25, 38], "cooldown": 1},
            {"name": "Judgement Flames", "damage": [28, 42], "cooldown": 2, "status_effect": "burn"},
            {"name": "Soul Sentence",    "damage": [32, 47], "cooldown": 2, "status_effect": "bleed"},
            {"name": "Wrath of Heaven",  "damage": [40, 58], "cooldown": 3, "status_effect": "stun"},
            {"name": "Final Execution",  "damage": [50, 70], "cooldown": 5},
        ],
        "reward_gold": 400,
        "reward_potions": 5,
        "relic_drop": "Judge's Seal",
    },
]
