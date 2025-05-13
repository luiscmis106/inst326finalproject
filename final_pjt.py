import sys
import random
import argparse

class Player: 
    """
    Represents a player in a game with health, coins, and actions like attacking and healing.

    Primary Author: Guy Saltsman
    Techniques Claimed:
    - Magic methods (__init__, __repr__)
    - Optional parameters and/or keyword arguments
    """
    def __init__(self, name, hp, max_hp, attack_power=0, heal_power=0):
        """
        Initializes a new player with name, health, attack power, and heal power.

        Parameters:
        - name (str): The name of the player.
        - hp (int): Starting health points.
        - max_hp (int): Maximum possible health points.
        - attack_power (int, optional): Extra damage added to base attacks. Defaults to 0.
        - heal_power (int, optional): Extra healing added to base heals. Defaults to 0.

        Primary Author: Guy Saltsman  
        Techniques Claimed:
        - Optional parameters and/or keyword arguments  
        - Magic method (__init__)
        """
        self.name = name
        self.health = hp
        self.max_hp = max_hp
        self.attack_power = attack_power
        self.heal_power = heal_power
        self.coins = 0
        self.is_computer = False

    def attack(self, base):
        """
        Calculates the total attack damage based on a base value and the player's attack power.

        Parameters:
        - base (int): The base damage.

        Returns:
        - int: Total damage dealt.

        Primary Author: Guy Saltsman
        """
        damage = base + self.attack_power
        return damage

    def heal(self, base):
        """
        Heals the player by a base amount plus any bonus from heal_power, 
        without exceeding max_hp.

        Parameters:
        - base (int): The base healing amount.

        Returns:
        - int: Actual amount healed.

        Primary Author: Guy Saltsman  
        """
        amount = base + self.heal_power
        self.health = min(self.max_hp, self.health + amount)
        return amount

    def is_alive(self):
        """
        Checks if the player is still alive (health > 0).

        Returns:
        - bool: True if alive, False otherwise.

        Primary Author: Guy Saltsman  
        """
        return self.health > 0

    def __repr__(self):
        """
        Returns a string representation of the player with name, current HP, max HP, and coins.

        Returns:
        - str: Player's status in formatted string.

        Primary Author: Guy Saltsman  
        Techniques Claimed:
        - Magic method (__repr__)  
        """
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
    """
    Manages the turn-based gameplay between two players including rolling, store interactions,
    healing, attacking, and win conditions.

    Primary Author: Gerardo Sandoval  
    Techniques Claimed:
    - f-strings  
    - Conditional expression 
    """
    
    def __init__(self, player1, player2):
        """
        Initializes a new game with two players.

        Parameters:
        - player1 (Player): The first player object.
        - player2 (Player): The second player object.

        Primary Author: Gerardo Sandoval  
        """
        self.player1 = player1
        self.player2 = player2

    def get_opponent(self, current):
        """
        Returns the opponent of the current player.

        Parameters:
        - current (Player): The player whose opponent is being requested.

        Returns:
        - Player: The opposing player.

        Primary Author: Gerardo Sandoval  
        Techniques Claimed:
        - Conditional expression
        """
        return self.player2 if current == self.player1 else self.player1

    def play_turn(self, player):
        """
        Executes a full turn for a player: rolls dice, adds coins, lets the player purchase an item
        from the store, and applies the item's effects.

        Parameters:
        - player (Player): The player whose turn is being played.

        Primary Author: Gerardo Sandoval  
        Techniques Claimed:
        - f-strings  
        - Conditional expression
        """
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
                print(f"{player.name} used {item['name']} and healed for +{healed} HP to {player.health} total HP.")
            elif item["type"] == "attack":
                opponent = self.get_opponent(player)
                opponent.health -= item["value"]
                print(f"{player.name} used {item['name']} and dealt -{item['value']} HP to {opponent.name}, bringing them to {opponent.health} HP.")
        else:
            print(f"{player.name} skipped their turn or made no valid purchase.")

        print(f"{player.name} → Health: {player.health}, Coins: {player.coins}")

    def play(self):
        """
        Runs the full game loop, alternating turns between the two players until one is defeated.

        Primary Author: Gerardo Sandoval  
        Techniques Claimed:
        - f-strings
        """
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
