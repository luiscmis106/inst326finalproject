import sys
import random
import argparse

class Player:
    def __init__(self, name, hp, max_hp, attack_power=0, heal_power=0):
        self.name = name
        self.health = hp
        self.max_hp = max_hp
        self.attack_power = attack_power
        self.heal_power = heal_power
        self.coins = 0
        self.is_computer = False

    def attack(self, base):
        damage = base + self.attack_power
        return damage

    def heal(self, base):
        amount = base + self.heal_power
        self.health = min(self.max_hp, self.health + amount)
        return amount

    def is_alive(self):
        return self.health > 0

    def __repr__(self):
        return f"{self.name} (HP: {self.health}/{self.max_hp}, Coins: {self.coins})"

class ComputerPlayer(Player):
    def __init__(self, name, hp, max_hp, attack_power=0, heal_power=0):
        super().__init__(name, hp, max_hp, attack_power, heal_power)
        self.is_computer = True

    def choose_item(self, items):
        affordable = [item for item in items if item["cost"] <= self.coins]
        return random.choice(affordable) if affordable else None

def dice_roll():
    return random.randint(1, 6)

STORE_ITEMS = [
    {"name": "Small Potion", "type": "heal", "cost": 1, "value": 5},
    {"name": "Medium Potion", "type": "heal", "cost": 3, "value": 15},
    {"name": "Large Potion", "type": "heal", "cost": 5, "value": 30},
    {"name": "Iron Blade", "type": "attack", "cost": 2, "value": 10},
    {"name": "Steel Blade", "type": "attack", "cost": 4, "value": 20},
    {"name": "Titan Blade", "type": "attack", "cost": 6, "value": 40},
]

def show_store(coins):
    print("\n-- Store --")
    for item in STORE_ITEMS:
        if item["cost"] <= coins:
            sign = "+" if item["type"] == "heal" else "-"
            print(f"{item['name']} ({item['type']}, {sign}{item['value']}): {item['cost']} coins")

def get_store_choice(player):
    show_store(player.coins)
    if player.is_computer:
        return player.choose_item(STORE_ITEMS)
    else:
        choice = input(f"{player.name}, choose an item to buy (or press enter to skip): ").strip()
        for item in STORE_ITEMS:
            if item["name"] == choice and item["cost"] <= player.coins:
                return item
        print("Invalid choice or not enough coins.")
        return None

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def get_opponent(self, current):
        return self.player2 if current == self.player1 else self.player1

    def play_turn(self, player):
        if not player.is_alive():
            return

        print(f"\n{player.name}'s turn:")
        roll = dice_roll()
        player.coins += roll
        print(f"{player.name} rolled a {roll} and received {roll} coins! Total coins: {player.coins}")

        item = get_store_choice(player)
        if item:
            player.coins -= item["cost"]
            if item["type"] == "heal":
                healed = player.heal(item["value"])
                print(f"{player.name} used {item['name']} and healed for +{healed} HP!") 
            elif item["type"] == "attack":
                opponent = self.get_opponent(player)
                opponent.health -= item["value"]
                print(f"{player.name} used {item['name']} and dealt -{item['value']} HP to {opponent.name}!")  
        else:
            print(f"{player.name} skipped their turn or made no valid purchase.")

        print(f"{player.name} → Health: {player.health}, Coins: {player.coins}")

    def play(self):
        print("\n-- Game Start --")
        while self.player1.is_alive() and self.player2.is_alive():
            self.play_turn(self.player1)
            if not self.player2.is_alive():
                print(f"\n{self.player1.name} wins!")
                break
            self.play_turn(self.player2)
            if not self.player1.is_alive():
                print(f"\n{self.player2.name} wins!")
                break

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, help="Enter your name")
    return parser.parse_args()

def main():
    args = parse_args()
    player1 = Player(args.name, hp=100, max_hp=100, attack_power=0, heal_power=0)
    player2 = ComputerPlayer("Computer", hp=100, max_hp=100, attack_power=0, heal_power=0)
    game = Game(player1, player2)
    game.play()

if __name__ == "__main__":
    main()
