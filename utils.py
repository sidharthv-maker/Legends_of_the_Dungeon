from data import CHARACTER_TEMPLATES, RELICS


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
    # Status effect indicators
    player_fx = _status_tag(player)
    enemy_fx  = _status_tag(enemy)
    print(f"{player.full_name()}{player_fx}")
    print(health_bar(player.hp, player.max_hp))
    print()
    print(f"{enemy.full_name()}{enemy_fx}")
    print(health_bar(enemy.hp, enemy.max_hp))
    clear_line()


def _status_tag(fighter):
    tags = []
    if fighter.burn_turns > 0:
        tags.append(f"BURN({fighter.burn_turns})")
    if fighter.bleed_stacks > 0:
        tags.append(f"BLEED({fighter.bleed_stacks})")
    if fighter.stun_turns > 0:
        tags.append(f"STUN({fighter.stun_turns})")
    return "  [" + " | ".join(tags) + "]" if tags else ""


def show_player_info(player):
    clear_line()
    print(f"Hero          : {player.full_name()}")
    print(f"HP            : {player.hp}/{player.max_hp}  (base: {player.base_max_hp})")
    print(f"Gold          : {player.gold}")
    print(f"Potions       : {player.potions}")
    print(f"Floor         : {player.floor}")
    print(f"Total Kills   : {player.wins}")
    print(f"Bosses Slain  : {player.bosses_defeated}")
    clear_line()

    # Champion upgrades
    cu = player.champion_upgrades
    print(f"Vitality      : Tier {cu['vitality']}/5  (+{cu['vitality'] * 15} max HP)")
    print(f"Ferocity      : Tier {cu['ferocity']}/5  (+{cu['ferocity'] * 10}% damage)")
    print(f"Fortune       : Tier {cu['fortune']}/5   (+{cu['fortune'] * 15}% gold)")
    clear_line()

    # Awakening & passive
    if player.awakened:
        passive = CHARACTER_TEMPLATES[player.name]["passive"]
        print(f"★ AWAKENED    : {passive['name']}")
        print(f"  {passive['description']}")
    else:
        needed = [s for s in ["vitality", "ferocity", "fortune"] if cu[s] < 3]
        print(f"Awakening     : Reach Tier 3 in {', '.join(needed)}")
    clear_line()

    # Relics
    if player.relics:
        print("Relics:")
        for relic_name in player.relics:
            relic = RELICS.get(relic_name, {})
            print(f"  • {relic_name} — {relic.get('description', '')}")
    else:
        print("Relics        : None  (defeat bosses to earn relics)")
    clear_line()

    # Attack upgrades
    print("Attack Levels:")
    for i, atk in enumerate(player.attacks):
        level = player.attack_levels[i]
        upgrade_bonus = level * 4
        low  = atk["damage"][0] + upgrade_bonus
        high = atk["damage"][1] + upgrade_bonus
        effect = atk.get("status_effect", "")
        effect_str = f"  ★ {effect.upper()}" if effect and level >= 3 else (f"  ({effect} at Lv3)" if effect else "")
        print(f"  {i + 1}. {atk['name']:<28} {low}-{high} dmg  Lv{level}/3{effect_str}")

    if not player.locked_attack_unlocked:
        locked = CHARACTER_TEMPLATES[player.name].get("locked_attack", {})
        remaining = sum(1 for j in range(len(CHARACTER_TEMPLATES[player.name]["attacks"])) if player.attack_levels[j] < 3)
        print(f"  [ LOCKED: {locked.get('name', '???')} — max all attacks ({remaining} remaining) ]")
    clear_line()
