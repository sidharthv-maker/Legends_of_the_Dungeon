import random
class Fighter:
    def __init__(self, name, max_hp, attacks, title=""):
        self.name = name
        self.title = title
        self.max_hp = max_hp
        self.hp = max_hp
        self.attacks = attacks
        self.attack_timers = [0] * len(attacks)
    def is_alive(self):
        return self.hp > 0
    def full_name(self):
        return f"{self.name}, {self.title}" if self.title else self.name
    def attack_target(self, attack_index, target):
        attack = self.attacks[attack_index]
        damage = random.randint(attack["damage"][0], attack["damage"][1])
        target.hp = max(0, target.hp - damage)
        self.attack_timers[attack_index] = attack.get("cooldown", 0)
        return attack["name"], damage
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
class Player(Fighter):
    def __init__(self, name, max_hp, attacks, title=""):
        super().__init__(name, max_hp, attacks, title)
        self.gold = 0
        self.potions = 3
        self.floor = 1
        self.wins = 0
        self.bosses_defeated = 0
    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attacks": self.attacks,
            "attack_timers": self.attack_timers,
            "gold": self.gold,
            "potions": self.potions,
            "floor": self.floor,
            "wins": self.wins,
            "bosses_defeated": self.bosses_defeated,
        }
    @classmethod
    def from_dict(cls, data):
        player = cls(
            name=data["name"],
            max_hp=data["max_hp"],
            attacks=data["attacks"],
            title=data.get("title", ""),
        )
        player.hp = data["hp"]
        player.attack_timers = data.get("attack_timers", [0] * len(player.attacks))
        player.gold = data["gold"]
        player.potions = data["potions"]
        player.floor = data["floor"]
        player.wins = data["wins"]
        player.bosses_defeated = data["bosses_defeated"]
        return player
class Enemy(Fighter):
    def __init__(self, name, max_hp, attacks, reward_gold=0, reward_potions=0, is_boss=False):
        super().__init__(name, max_hp, attacks)
        self.reward_gold = reward_gold
        self.reward_potions = reward_potions
        self.is_boss = is_boss