def clear_line():
    print("-" * 50)
def pause():
    input("\nPress Enter to continue...")
def ask_int(prompt, low, high):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            number = int(value)
            if low <= number <= high:
                return number
        print(f"Enter a number between {low} and {high}.")
def health_bar(current, maximum, bar_length=20):
    ratio = current / maximum if maximum > 0 else 0
    filled = int(ratio * bar_length)
    empty = bar_length - filled
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {current}/{maximum}"
def show_status(player, enemy):
    clear_line()
    print(player.full_name())
    print(health_bar(player.hp, player.max_hp))
    print()
    print(enemy.full_name())
    print(health_bar(enemy.hp, enemy.max_hp))
    clear_line()
def show_player_info(player):
    clear_line()
    print(f"Hero: {player.full_name()}")
    print(f"HP: {player.hp}/{player.max_hp}")
    print(f"Gold: {player.gold}")
    print(f"Potions: {player.potions}")
    print(f"Floor: {player.floor}")
    print(f"Wins: {player.wins}")
    print(f"Bosses Defeated: {player.bosses_defeated}")
    clear_line()