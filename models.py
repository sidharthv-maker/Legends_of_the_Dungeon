import random


class Fighter:
    def __init__(self, name, max_hp, attacks, title=""):
        self.name = name
        self.title = title
        self.max_hp = max_hp
        self.hp = max_hp
        self.attacks = attacks
        self.attack_timers = [0] * len(attacks)
        # Status effects
        self.burn_turns = 0    # turns of burn remaining
        self.bleed_stacks = 0  # stacks of bleed (max 3)
        self.stun_turns = 0    # turns of stun remaining

    def is_alive(self):
        return self.hp > 0

    def full_name(self):
        return f"{self.name}, {self.title}" if self.title else self.name

    def receive_damage(self, amount):
        """Apply damage. Returns True if Undying passive triggered (Player only)."""
        self.hp = max(0, self.hp - amount)
        return False

    def attack_target(self, attack_index, target):
        attack = self.attacks[attack_index]
        damage = random.randint(attack["damage"][0], attack["damage"][1])
        undying = target.receive_damage(damage)
        self.attack_timers[attack_index] = attack.get("cooldown", 0)
        return attack["name"], damage, undying

    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    def reduce_cooldowns(self):
        for i in range(len(self.attack_timers)):
            if self.attack_timers[i] > 0:
                self.attack_timers[i] -= 1

    def attack_ready(self, index):
        return self.attack_timers[index] == 0

    def available_attack_indices(self):
        return [i for i in range(len(self.attacks)) if self.attack_ready(i)]

    def apply_status_effect(self, effect_type, burn_damage=5):
        """Apply a status effect to this fighter."""
        if effect_type == "burn":
            self.burn_turns = max(self.burn_turns, 2)
            self.burn_damage_per_tick = burn_damage
        elif effect_type == "stun":
            self.stun_turns = max(self.stun_turns, 1)
        elif effect_type == "bleed":
            self.bleed_stacks = min(3, self.bleed_stacks + 1)

    def consume_stun(self):
        """Returns True if stunned this turn, then decrements the counter."""
        if self.stun_turns > 0:
            self.stun_turns -= 1
            return True
        return False

    def process_status_effects(self):
        """
        Apply damage from active status effects at the start of a turn.
        Returns (total_damage, list_of_messages).
        """
        total = 0
        messages = []

        if self.burn_turns > 0:
            dmg = getattr(self, "burn_damage_per_tick", 5)
            total += dmg
            self.burn_turns -= 1
            remaining = f"{self.burn_turns} turn(s) left" if self.burn_turns > 0 else "faded"
            messages.append(f"  [BURN] {self.full_name()} takes {dmg} fire damage! ({remaining})")

        if self.bleed_stacks > 0:
            dmg = self.bleed_stacks * 3
            total += dmg
            messages.append(f"  [BLEED] {self.full_name()} bleeds for {dmg} damage! ({self.bleed_stacks} stack(s))")

        if total > 0:
            self.hp = max(0, self.hp - total)

        return total, messages


class Player(Fighter):
    def __init__(self, name, max_hp, attacks, title=""):
        super().__init__(name, max_hp, attacks, title)
        self.base_max_hp = max_hp        # before vitality / relic bonuses
        self.gold = 0
        self.potions = 3
        self.floor = 1
        self.wins = 0
        self.bosses_defeated = 0
        # Progression
        self.attack_levels = [0] * len(attacks)
        self.champion_upgrades = {"vitality": 0, "ferocity": 0, "fortune": 0}
        self.relics = []
        self.locked_attack_unlocked = False
        # Per-run passive state (reset each dungeon run)
        self.undying_used = False
        self.consecutive_hits = 0

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def awakened(self):
        """True when all three champion stats reach tier 3."""
        return all(self.champion_upgrades[k] >= 3 for k in ["vitality", "ferocity", "fortune"])

    # ── Damage & passives ─────────────────────────────────────────────────────

    def receive_damage(self, amount):
        """Apply damage, checking Larry's Undying passive first."""
        if self.awakened and self.name == "Larry" and not self.undying_used:
            if self.hp - amount <= 0 and self.hp > 1:
                self.hp = 1
                self.undying_used = True
                return True   # signals Undying triggered
        self.hp = max(0, self.hp - amount)
        return False

    def attack_target(self, attack_index, target):
        attack = self.attacks[attack_index]
        level = self.attack_levels[attack_index]
        upgrade_bonus = level * 4   # +4 to both min and max per upgrade level

        base_min = attack["damage"][0] + upgrade_bonus
        base_max = attack["damage"][1] + upgrade_bonus

        # Orion Precision: 25% chance for max damage
        if self.awakened and self.name == "Orion" and random.random() < 0.25:
            damage = base_max
        else:
            damage = random.randint(base_min, base_max)

        # Akira Shadow Step: every 3rd consecutive attack = double damage
        if self.awakened and self.name == "Akira":
            self.consecutive_hits += 1
            if self.consecutive_hits % 3 == 0:
                damage *= 2

        # Drakon Infernal Rage: below 30% HP = +50% damage
        if self.awakened and self.name == "Drakon" and self.hp / self.max_hp < 0.30:
            damage = int(damage * 1.5)

        # Ferocity multiplier
        ferocity = self.champion_upgrades["ferocity"]
        damage = int(damage * (1 + 0.10 * ferocity))

        undying = target.receive_damage(damage)
        self.attack_timers[attack_index] = attack.get("cooldown", 0)

        # Status effect triggers only at upgrade level 3
        if level >= 3:
            effect = attack.get("status_effect")
            if effect:
                burn_dmg = 5 + self._get_burn_bonus() if effect == "burn" else 5
                target.apply_status_effect(effect, burn_damage=burn_dmg)

        return attack["name"], damage, undying

    def _get_burn_bonus(self):
        """Extra burn damage per tick from the Infernal Ember relic."""
        from data import RELICS
        return sum(RELICS.get(r, {}).get("burn_bonus", 0) for r in self.relics)

    # ── Upgrade methods ───────────────────────────────────────────────────────

    def upgrade_attack(self, attack_index):
        """
        Attempt to upgrade an attack by one level.
        Returns: cost paid (int), or 0 if not enough gold, or -1 if already max.
        """
        from data import ATTACK_UPGRADE_COSTS
        level = self.attack_levels[attack_index]
        if level >= 3:
            return -1
        cost = ATTACK_UPGRADE_COSTS[level]
        if self.gold < cost:
            return 0
        self.gold -= cost
        self.attack_levels[attack_index] += 1
        self._check_locked_attack_unlock()
        return cost

    def _check_locked_attack_unlock(self):
        """Unlock the hidden 6th attack when all base attacks hit level 3."""
        from data import CHARACTER_TEMPLATES
        if self.locked_attack_unlocked:
            return
        base_count = len(CHARACTER_TEMPLATES[self.name]["attacks"])
        if all(self.attack_levels[i] >= 3 for i in range(base_count)):
            locked = CHARACTER_TEMPLATES[self.name].get("locked_attack")
            if locked:
                self.attacks.append(dict(locked))
                self.attack_levels.append(0)
                self.attack_timers.append(0)
                self.locked_attack_unlocked = True

    def upgrade_champion_stat(self, stat):
        """
        Upgrade vitality / ferocity / fortune by one tier.
        Returns: cost paid (int), or 0 if not enough gold, or -1 if already tier 5.
        """
        from data import CHAMPION_UPGRADE_COSTS, RELICS
        tier = self.champion_upgrades[stat]
        if tier >= 5:
            return -1
        cost = CHAMPION_UPGRADE_COSTS[stat][tier]
        if self.gold < cost:
            return 0
        self.gold -= cost
        self.champion_upgrades[stat] += 1
        if stat == "vitality":
            bonus_hp = 15
            self.base_max_hp += bonus_hp
            # Recalculate max_hp including existing relic bonuses
            relic_hp = sum(RELICS.get(r, {}).get("bonus_hp", 0) for r in self.relics)
            self.max_hp = self.base_max_hp + relic_hp
        return cost

    def gain_relic(self, relic_name):
        """
        Add a relic to the player. Returns True on success, False if slots full
        or already owned.
        """
        from data import RELICS
        if len(self.relics) >= 3 or relic_name in self.relics:
            return False
        self.relics.append(relic_name)
        relic = RELICS.get(relic_name, {})
        if "bonus_hp" in relic:
            self.base_max_hp += relic["bonus_hp"]
            self.max_hp += relic["bonus_hp"]
            self.hp = min(self.hp + relic["bonus_hp"], self.max_hp)
        return True

    # ── Run management ────────────────────────────────────────────────────────

    def reset_for_new_run(self):
        """Reset per-run state when entering a new dungeon."""
        self.hp = self.max_hp
        self.floor = 1
        self.potions = 3
        self.attack_timers = [0] * len(self.attacks)
        self.undying_used = False
        self.consecutive_hits = 0
        self.burn_turns = 0
        self.bleed_stacks = 0
        self.stun_turns = 0

    # ── Serialisation ─────────────────────────────────────────────────────────

    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "base_max_hp": self.base_max_hp,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attacks": self.attacks,
            "attack_timers": self.attack_timers,
            "gold": self.gold,
            "potions": self.potions,
            "floor": self.floor,
            "wins": self.wins,
            "bosses_defeated": self.bosses_defeated,
            "attack_levels": self.attack_levels,
            "champion_upgrades": self.champion_upgrades,
            "relics": self.relics,
            "locked_attack_unlocked": self.locked_attack_unlocked,
            "undying_used": self.undying_used,
            "consecutive_hits": self.consecutive_hits,
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(
            name=data["name"],
            max_hp=data["max_hp"],
            attacks=data["attacks"],
            title=data.get("title", ""),
        )
        player.base_max_hp = data.get("base_max_hp", data["max_hp"])
        player.hp = data["hp"]
        player.attack_timers = data.get("attack_timers", [0] * len(player.attacks))
        player.gold = data["gold"]
        player.potions = data["potions"]
        player.floor = data["floor"]
        player.wins = data["wins"]
        player.bosses_defeated = data["bosses_defeated"]
        player.attack_levels = data.get("attack_levels", [0] * len(player.attacks))
        player.champion_upgrades = data.get(
            "champion_upgrades", {"vitality": 0, "ferocity": 0, "fortune": 0}
        )
        player.relics = data.get("relics", [])
        player.locked_attack_unlocked = data.get("locked_attack_unlocked", False)
        player.undying_used = data.get("undying_used", False)
        player.consecutive_hits = data.get("consecutive_hits", 0)
        return player


class Enemy(Fighter):
    def __init__(self, name, max_hp, attacks,
                 reward_gold=0, reward_potions=0,
                 is_boss=False, relic_drop=None):
        super().__init__(name, max_hp, attacks)
        self.reward_gold = reward_gold
        self.reward_potions = reward_potions
        self.is_boss = is_boss
        self.relic_drop = relic_drop   # relic name string, or None
