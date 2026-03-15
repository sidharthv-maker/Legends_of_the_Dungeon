import os
import random

from data import BOSSES, CHARACTER_TEMPLATES, REGULAR_ENEMIES, SAVE_FILE
from models import Enemy, Player
from save_system import delete_save, load_game, save_game
from utils import ask_int, clear_line, pause, show_player_info, show_status
def choose_character():
    print("\nChoose your character:\n")
    names = list(CHARACTER_TEMPLATES.keys())

    for i, name in enumerate(names, start=1):
        info = CHARACTER_TEMPLATES[name]
        print(f"{i}. {name}, {info['title']} (HP: {info['max_hp']})")

    choice = ask_int("\nEnter choice: ", 1, len(names))
    selected_name = names[choice - 1]
    info = CHARACTER_TEMPLATES[selected_name]

    return Player(
        name=selected_name,
        title=info["title"],
        max_hp=info["max_hp"],
        attacks=info["attacks"],
    )
def create_regular_enemy(floor):
    template = random.choice(REGULAR_ENEMIES)
    bonus_hp = (floor - 1) * 8
    scaled_attacks = []
    for atk in template["attacks"]:
        scaled_attacks.append(
            {
                "name": atk["name"],
                "damage": [
                    atk["damage"][0] + (floor - 1) * 2,
                    atk["damage"][1] + (floor - 1) * 2,
                ],
                "cooldown": atk.get("cooldown", 0),
            }
        )
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
    scaled_attacks = []
    for atk in boss_template["attacks"]:
        scaled_attacks.append(
            {
                "name": atk["name"],
                "damage": [atk["damage"][0] + floor, atk["damage"][1] + floor],
                "cooldown": atk.get("cooldown", 0),
            }
        )
    return Enemy(
        name=boss_template["name"],
        max_hp=boss_template["max_hp"] + bonus_hp,
        attacks=scaled_attacks,
        reward_gold=boss_template["reward_gold"] + floor * 10,
        reward_potions=boss_template["reward_potions"],
        is_boss=True,
    )
def generate_enemy_for_floor(floor):
    return create_boss(floor) if floor % 3 == 0 else create_regular_enemy(floor)

def player_turn(player, enemy):
    player.reduce_cooldowns()
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
                low, high = atk["damage"]
                cd_left = player.attack_timers[i - 1]
                status = "READY" if cd_left == 0 else f"Cooldown: {cd_left} turn(s)"
                print(f"{i}. {atk['name']} ({low}-{high} dmg) [{status}]")
            attack_choice = ask_int("\nAttack number: ", 1, len(player.attacks))
            attack_index = attack_choice - 1
            if not player.attack_ready(attack_index):
                print("\nThat attack is still on cooldown.")
                pause()
                continue
            attack_name, damage = player.attack_target(attack_index, enemy)
            print(f"\n{player.full_name()} used {attack_name}!")
            print(f"It dealt {damage} damage to {enemy.full_name()}!")
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
    available = enemy.available_attack_indices() or [0]
    attack_index = random.choice(available)
    attack_name, damage = enemy.attack_target(attack_index, player)

    print(f"\n{enemy.full_name()} used {attack_name}!")
    print(f"It dealt {damage} damage to {player.full_name()}!")
    show_status(player, enemy)
def reward_player(player, enemy):
    player.gold += enemy.reward_gold
    player.potions += enemy.reward_potions
    player.wins += 1
    if enemy.is_boss:
        player.bosses_defeated += 1
    print("\nVictory!")
    print(f"You gained {enemy.reward_gold} gold.")
    if enemy.reward_potions > 0:
        print(f"You found {enemy.reward_potions} potion(s).")
    else:
        print("You found no potions.")
    player.attack_timers = [0] * len(player.attacks)
def post_battle_recovery(player):
    recovery = random.randint(12, 22)
    actual = player.heal(recovery)
    print(f"\nAfter the battle, you recover {actual} HP by resting.")
def battle(player, enemy):
    clear_line()
    if enemy.is_boss:
        print(f"BOSS FIGHT! {enemy.full_name()} stands before you!")
    else:
        print(f"A wild {enemy.full_name()} appears!")
    clear_line()
    show_status(player, enemy)
    while player.is_alive() and enemy.is_alive():
        player_turn(player, enemy)
        if enemy.is_alive():
            pause()
            enemy_turn(enemy, player)
            pause()
    if player.is_alive():
        reward_player(player, enemy)
        return True
    return False
def dungeon_mode(player):
    while player.is_alive():
        clear_line()
        print(f"DUNGEON FLOOR {player.floor}")
        clear_line()
        enemy = generate_enemy_for_floor(player.floor)
        won = battle(player, enemy)
        if not won:
            print(f"\n{player.full_name()} has fallen in the dungeon...")
            print(f"You reached floor {player.floor}.")
            print(f"Total wins: {player.wins}")
            print(f"Bosses defeated: {player.bosses_defeated}")
            if os.path.exists(SAVE_FILE):
                print("\nTip: you can load your saved game from the main menu.")
            return
        post_battle_recovery(player)
        player.floor += 1
        save_game(player)
        clear_line()
        print("What would you like to do now?")
        print("1. Continue deeper into the dungeon")
        print("2. Return to main menu")
        choice = ask_int("\nChoose: ", 1, 2)
        if choice == 2:
            print("\nReturning to main menu...")
            return
def new_game():
    player = choose_character()
    print(f"\nYou chose {player.full_name()}!")
    pause()
    dungeon_mode(player)
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
            new_game()
        elif choice == 2:
            player = load_game()
            if player is not None:
                pause()
                dungeon_mode(player)
            else:
                pause()
        elif choice == 3:
            delete_save()
            pause()
        else:
            print("\nGoodbye, hero.")
            break