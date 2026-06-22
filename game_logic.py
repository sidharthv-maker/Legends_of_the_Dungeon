import os
import random

from data import (
    ATTACK_UPGRADE_COSTS, BOSSES, CHAMPION_UPGRADE_COSTS,
    CHARACTER_TEMPLATES, REGULAR_ENEMIES, RELICS, SAVE_FILE,
)
from models import Enemy, Player
from save_system import delete_save, load_game, save_game
from utils import ask_int, clear_line, pause, show_player_info, show_status


# ── Enemy factories ───────────────────────────────────────────────────────────

def create_regular_enemy(floor):
    template = random.choice(REGULAR_ENEMIES)
    bonus_hp = (floor - 1) * 8
    scaled_attacks = [
        {
            "name": atk["name"],
            "damage": [
                atk["damage"][0] + (floor - 1) * 2,
                atk["damage"][1] + (floor - 1) * 2,
            ],
            "cooldown": atk.get("cooldown", 0),
        }
        for atk in template["attacks"]
    ]
    return Enemy(
        name=template["name"],
        max_hp=template["max_hp"] + bonus_hp,
        attacks=scaled_attacks,
        reward_gold=template["reward_gold"] + (floor - 1) * 5,
        reward_potions=template["reward_potions"] if random.random() < 0.7 else 0,
        is_boss=False,
    )


def create_boss(floor):
    boss_template = BOSSES[(floor // 3 - 1) % len(BOSSES)]
    bonus_hp = (floor - 3) * 10 if floor > 3 else 0
    scaled_attacks = [
        {
            "name": atk["name"],
            "damage": [atk["damage"][0] + floor, atk["damage"][1] + floor],
            "cooldown": atk.get("cooldown", 0),
        }
        for atk in boss_template["attacks"]
    ]
    return Enemy(
        name=boss_template["name"],
        max_hp=boss_template["max_hp"] + bonus_hp,
        attacks=scaled_attacks,
        reward_gold=boss_template["reward_gold"] + floor * 10,
        reward_potions=boss_template["reward_potions"],
        is_boss=True,
        relic_drop=boss_template.get("relic_drop"),
    )


def generate_enemy_for_floor(floor):
    return create_boss(floor) if floor % 3 == 0 else create_regular_enemy(floor)


# ── Battle helpers ────────────────────────────────────────────────────────────

def _print_status_messages(messages):
    for msg in messages:
        print(msg)


def player_turn(player, enemy):
    player.reduce_cooldowns()

    # Status effects tick at the start of player's turn
    _, msgs = player.process_status_effects()
    if msgs:
        _print_status_messages(msgs)
        if not player.is_alive():
            return   # player died from status damage

    # Stun check
    if player.consume_stun():
        print(f"\n{player.full_name()} is stunned and loses their turn!")
        pause()
        return

    while True:
        show_status(player, enemy)
        print("\nYour actions:")
        print("1. Attack")
        print("2. Use Potion")
        print("3. Save Game")
        print("4. View Hero Info")
        action = ask_int("\nChoose action: ", 1, 4)

        if action == 1:
            print("\nChoose an attack:\n")
            for i, atk in enumerate(player.attacks, start=1):
                level = player.attack_levels[i - 1]
                upgrade_bonus = level * 4
                low  = atk["damage"][0] + upgrade_bonus
                high = atk["damage"][1] + upgrade_bonus
                cd   = player.attack_timers[i - 1]
                status_str  = "READY" if cd == 0 else f"Cooldown: {cd}"
                level_str   = f"Lv{level}" if level > 0 else "  "
                effect      = atk.get("status_effect", "")
                effect_str  = f" [{effect.upper()}]" if effect and level >= 3 else ""
                locked_str  = " [LOCKED ATK]" if atk.get("name") == CHARACTER_TEMPLATES[player.name].get("locked_attack", {}).get("name") else ""
                print(f"{i}. {atk['name']:<28} {low}-{high} dmg  {level_str}{effect_str}  [{status_str}]{locked_str}")

            attack_choice = ask_int("\nAttack number: ", 1, len(player.attacks))
            attack_index  = attack_choice - 1

            if not player.attack_ready(attack_index):
                print("\nThat attack is still on cooldown.")
                pause()
                continue

            attack_name, damage, undying = player.attack_target(attack_index, enemy)
            print(f"\n{player.full_name()} used {attack_name}!")

            # Zara Chain Lightning passive
            if player.awakened and player.name == "Zara" and random.random() < 0.30:
                chain_dmg = damage // 2
                enemy.receive_damage(chain_dmg)
                print(f"Chain Lightning! A second bolt deals {chain_dmg} damage!")

            print(f"Total damage dealt: {damage}")

            # Status effect notification
            effect = player.attacks[attack_index].get("status_effect")
            if effect and player.attack_levels[attack_index] >= 3:
                print(f"  ★ {effect.capitalize()} applied to {enemy.full_name()}!")

            show_status(player, enemy)
            return

        if action == 2:
            if player.potions <= 0:
                print("\nYou have no potions left.")
                pause()
                continue
            heal_amount = random.randint(25, 40)
            actual = player.heal(heal_amount)
            player.potions -= 1
            print(f"\nYou used a potion and restored {actual} HP.")
            print(f"Potions left: {player.potions}")
            show_status(player, enemy)
            pause()
            return

        if action == 3:
            save_game(player)
            pause()
            continue

        if action == 4:
            show_player_info(player)
            pause()


def enemy_turn(enemy, player):
    enemy.reduce_cooldowns()

    # Status effects tick at start of enemy's turn
    _, msgs = enemy.process_status_effects()
    if msgs:
        _print_status_messages(msgs)

    if not enemy.is_alive():
        return

    # Stun check
    if enemy.consume_stun():
        print(f"\n{enemy.full_name()} is stunned and loses their turn!")
        return

    available = enemy.available_attack_indices() or [0]
    attack_index = random.choice(available)
    attack_name, damage, undying = enemy.attack_target(attack_index, player)

    print(f"\n{enemy.full_name()} used {attack_name}!")
    if undying:
        print(f"  ★ UNDYING — {player.full_name()} survives the blow at 1 HP!")
    else:
        print(f"It dealt {damage} damage to {player.full_name()}!")
    show_status(player, enemy)


def reward_player(player, enemy):
    # Fortune multiplier
    fortune = player.champion_upgrades["fortune"]
    gold_multiplier = 1 + 0.15 * fortune
    gold_earned = int(enemy.reward_gold * gold_multiplier)

    player.gold += gold_earned
    player.potions += enemy.reward_potions
    player.wins += 1
    if enemy.is_boss:
        player.bosses_defeated += 1

    print("\nVictory!")
    print(f"You gained {gold_earned} gold." + (f" (Fortune x{gold_multiplier:.2f})" if fortune > 0 else ""))
    if enemy.reward_potions > 0:
        print(f"You found {enemy.reward_potions} potion(s).")

    # Arthur Valor passive: heal on kill
    if player.awakened and player.name == "Arthur":
        healed = player.heal(12)
        print(f"  ★ Valor — {player.full_name()} recovers {healed} HP from the kill!")

    # Relic drop from boss
    if enemy.is_boss and enemy.relic_drop:
        relic_name = enemy.relic_drop
        if relic_name not in player.relics and len(player.relics) < 3:
            player.gain_relic(relic_name)
            relic = RELICS[relic_name]
            clear_line()
            print(f"  ★ RELIC OBTAINED: {relic_name}")
            print(f"     {relic['description']}")
            clear_line()
        elif relic_name in player.relics:
            print(f"  (You already own {relic_name}.)")
        else:
            print(f"  (Relic slots full — {relic_name} lost.)")

    player.attack_timers = [0] * len(player.attacks)


def post_battle_recovery(player):
    recovery = random.randint(12, 22)
    actual = player.heal(recovery)
    print(f"\nAfter the battle, you recover {actual} HP by resting.")


def battle(player, enemy):
    clear_line()
    if enemy.is_boss:
        print(f"  ★ BOSS FIGHT!  {enemy.full_name()} stands before you! ★")
    else:
        print(f"A wild {enemy.full_name()} appears!")
    clear_line()
    show_status(player, enemy)

    while player.is_alive() and enemy.is_alive():
        player_turn(player, enemy)
        if enemy.is_alive() and player.is_alive():
            pause()
            enemy_turn(enemy, player)
            pause()

    if player.is_alive():
        reward_player(player, enemy)
        return True
    return False


# ── Dungeon run ───────────────────────────────────────────────────────────────

def dungeon_mode(player):
    player.reset_for_new_run()
    print(f"\nEntering the dungeon as {player.full_name()}...")
    if player.awakened:
        passive = CHARACTER_TEMPLATES[player.name]["passive"]
        print(f"  ★ Passive active: {passive['name']} — {passive['description']}")
    pause()

    while player.is_alive():
        clear_line()
        print(f"DUNGEON FLOOR {player.floor}")
        clear_line()
        enemy = generate_enemy_for_floor(player.floor)
        won = battle(player, enemy)

        if not won:
            clear_line()
            print(f"\n{player.full_name()} has fallen in the dungeon...")
            print(f"Reached floor : {player.floor}")
            print(f"Total kills   : {player.wins}")
            print(f"Bosses slain  : {player.bosses_defeated}")
            print(f"Gold carried  : {player.gold}  (kept)")
            clear_line()
            return

        post_battle_recovery(player)
        player.floor += 1
        save_game(player)

        clear_line()
        print("What would you like to do?")
        print("1. Continue deeper into the dungeon")
        print("2. Exit dungeon (keep gold, go to hub)")
        choice = ask_int("\nChoose: ", 1, 2)
        if choice == 2:
            print("\nYou leave the dungeon, gold in hand.")
            return


# ── Upgrade menus (hub only) ──────────────────────────────────────────────────

def upgrade_attacks_menu(player):
    from data import CHARACTER_TEMPLATES as CT
    while True:
        clear_line()
        print(f"=== UPGRADE ATTACKS ===   Gold: {player.gold}")
        clear_line()
        all_maxed = True
        for i, atk in enumerate(player.attacks):
            level = player.attack_levels[i]
            upgrade_bonus = level * 4
            low  = atk["damage"][0] + upgrade_bonus
            high = atk["damage"][1] + upgrade_bonus
            effect = atk.get("status_effect", "")

            if level < 3:
                all_maxed = False
                next_cost = ATTACK_UPGRADE_COSTS[level]
                cost_str = f"→ Lv{level + 1} for {next_cost}g"
            else:
                cost_str = "[MAX]"

            effect_str = f" ★ {effect.upper()} unlocked" if effect and level >= 3 else (
                f" ({effect} at Lv3)" if effect else ""
            )
            print(f"{i + 1}. {atk['name']:<28} {low}-{high} dmg  Lv{level}  {cost_str}{effect_str}")

        if not player.locked_attack_unlocked:
            base_count = len(CT[player.name]["attacks"])
            locked = CT[player.name].get("locked_attack", {})
            remaining = sum(1 for j in range(base_count) if player.attack_levels[j] < 3)
            print(f"\n  [ LOCKED ATTACK: {locked.get('name', '???')} — max all attacks to unlock ({remaining} remaining) ]")

        if all_maxed and not player.locked_attack_unlocked:
            print("\n  ★ All attacks maxed! Locked attack unlocked!")

        print(f"\n{len(player.attacks) + 1}. Back")
        choice = ask_int("\nUpgrade attack number (or Back): ", 1, len(player.attacks) + 1)

        if choice == len(player.attacks) + 1:
            return

        idx = choice - 1
        result = player.upgrade_attack(idx)
        if result == -1:
            print("\nThat attack is already at max level.")
        elif result == 0:
            print(f"\nNot enough gold. You need {ATTACK_UPGRADE_COSTS[player.attack_levels[idx]]}g.")
        else:
            atk_name = player.attacks[idx]["name"]
            print(f"\n{atk_name} upgraded to Lv{player.attack_levels[idx]}!")
            if player.locked_attack_unlocked and len(player.attacks) == len(CT[player.name]["attacks"]) + 1:
                locked_name = player.attacks[-1]["name"]
                clear_line()
                print(f"  ★ LOCKED ATTACK UNLOCKED: {locked_name}!")
                clear_line()
        save_game(player)
        pause()


def upgrade_champion_menu(player):
    while True:
        clear_line()
        print(f"=== CHAMPION UPGRADES ===   Gold: {player.gold}")
        print("  (+15 max HP / tier   |   +10% damage / tier   |   +15% gold / tier)")
        clear_line()

        stats = ["vitality", "ferocity", "fortune"]
        labels = {
            "vitality": f"Vitality  (Max HP now: {player.max_hp})",
            "ferocity": f"Ferocity  (Damage ×{1 + 0.10 * player.champion_upgrades['ferocity']:.2f})",
            "fortune":  f"Fortune   (Gold ×{1 + 0.15 * player.champion_upgrades['fortune']:.2f})",
        }
        for i, stat in enumerate(stats, start=1):
            tier = player.champion_upgrades[stat]
            if tier < 5:
                cost = CHAMPION_UPGRADE_COSTS[stat][tier]
                cost_str = f"→ Tier {tier + 1} for {cost}g"
            else:
                cost_str = "[MAX]"
            print(f"{i}. {labels[stat]:<40} Tier {tier}/5  {cost_str}")

        awakening_tiers = [player.champion_upgrades[s] for s in stats]
        if player.awakened:
            passive = CHARACTER_TEMPLATES[player.name]["passive"]
            print(f"\n  ★ AWAKENED — Passive active: {passive['name']}")
        else:
            needed = [s for s in stats if player.champion_upgrades[s] < 3]
            print(f"\n  [ Awakening: reach Tier 3 in {', '.join(needed)} to unlock your passive ]")

        print("\n4. Back")
        choice = ask_int("\nUpgrade stat (or Back): ", 1, 4)
        if choice == 4:
            return

        stat = stats[choice - 1]
        was_awakened = player.awakened
        result = player.upgrade_champion_stat(stat)

        if result == -1:
            print(f"\n{stat.capitalize()} is already at max tier.")
        elif result == 0:
            tier = player.champion_upgrades[stat]
            print(f"\nNot enough gold. You need {CHAMPION_UPGRADE_COSTS[stat][tier]}g.")
        else:
            print(f"\n{stat.capitalize()} upgraded to Tier {player.champion_upgrades[stat]}!")
            if not was_awakened and player.awakened:
                passive = CHARACTER_TEMPLATES[player.name]["passive"]
                clear_line()
                print(f"  ★ ★ ★  AWAKENING ACHIEVED  ★ ★ ★")
                print(f"  {player.full_name()} has awakened their true power!")
                print(f"  Passive unlocked: {passive['name']}")
                print(f"  {passive['description']}")
                clear_line()

        save_game(player)
        pause()


# ── Hub ───────────────────────────────────────────────────────────────────────

def hub_menu(player):
    while True:
        clear_line()
        print(f"=== HUB — {player.full_name()} ===")
        print(f"  Gold: {player.gold}   Wins: {player.wins}   Bosses Slain: {player.bosses_defeated}")
        if player.awakened:
            passive = CHARACTER_TEMPLATES[player.name]["passive"]
            print(f"  ★ Awakened — {passive['name']}: {passive['description']}")
        if player.relics:
            print(f"  Relics: {', '.join(player.relics)}")
        clear_line()
        print("1. Enter Dungeon")
        print("2. Upgrade Attacks")
        print("3. Upgrade Champion")
        print("4. View Full Status")
        print("5. Save & Quit")

        choice = ask_int("\nChoose: ", 1, 5)
        if choice == 1:
            dungeon_mode(player)
        elif choice == 2:
            upgrade_attacks_menu(player)
        elif choice == 3:
            upgrade_champion_menu(player)
        elif choice == 4:
            show_player_info(player)
            pause()
        elif choice == 5:
            save_game(player)
            print("\nProgress saved. See you next time, hero.")
            return


# ── Character selection ───────────────────────────────────────────────────────

def choose_character():
    print("\nChoose your character:\n")
    names = list(CHARACTER_TEMPLATES.keys())
    for i, name in enumerate(names, start=1):
        info = CHARACTER_TEMPLATES[name]
        passive = info["passive"]
        print(f"{i}. {name}, {info['title']}  (HP: {info['max_hp']})")
        print(f"   Passive: {passive['name']} — {passive['description']}")
    choice = ask_int("\nEnter choice: ", 1, len(names))
    selected = names[choice - 1]
    info = CHARACTER_TEMPLATES[selected]
    return Player(
        name=selected,
        title=info["title"],
        max_hp=info["max_hp"],
        attacks=[dict(a) for a in info["attacks"]],
    )


# ── Main menu ─────────────────────────────────────────────────────────────────

def main_menu():
    while True:
        clear_line()
        print("=== LEGENDS OF THE DUNGEON ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Delete Save")
        print("4. Quit")
        clear_line()
        choice = ask_int("Choose an option: ", 1, 4)

        if choice == 1:
            if os.path.exists(SAVE_FILE):
                clear_line()
                print("WARNING: A save file already exists.")
                print("Starting a new game will permanently erase all progress.")
                clear_line()
                print("1. Yes, start new game (delete existing save)")
                print("2. Cancel")
                confirm = ask_int("Confirm: ", 1, 2)
                if confirm == 2:
                    continue
                delete_save()
            player = choose_character()
            print(f"\nYou chose {player.full_name()}!")
            pause()
            hub_menu(player)

        elif choice == 2:
            player = load_game()
            if player is not None:
                pause()
                hub_menu(player)
            else:
                pause()

        elif choice == 3:
            delete_save()
            pause()

        else:
            print("\nGoodbye, hero.")
            break
