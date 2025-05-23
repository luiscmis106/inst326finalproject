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
    """
    A subclass of Player that represents an AI-controlled opponent.

    The ComputerPlayer automatically selects items during its turn,
    preferring high-value attack items if affordable, and falling back
    on healing items or a random choice otherwise.

    Primary Author: Tysen Wills  
    Techniques Claimed:
    - method overriding using super()
    """
    
    def __init__(self, name, hp, max_hp, attack_power=0, heal_power=0):
        """
        Initializes the computer player.

        Parameters:
        - name (str): The name of the computer player.
        - hp (int): Starting health points.
        - max_hp (int): Maximum possible health points.
        - attack_power (int, optional): Additional damage added to attacks.
        - heal_power (int, optional): Additional healing power.

        Primary Author: Tysen Wills  
        """
        super().__init__(name, hp, max_hp, attack_power, heal_power)
        self.is_computer = True

    def choose_item(self, items):
        """
        Selects the most valuable item from the store.

        Preference goes to attack items. If no attack items are
        affordable, the highest-value healing item is selected. If neither
        are available, a random affordable item is chosen.

        Parameters:
        - items (list of dict): List of store items, each with keys: 'name', 'type', 'cost', 'value'.

        Returns:
        - dict or None: The selected item dictionary, or None if no items are affordable.

        Primary Author: Tysen Wills  
        """
        affordable = [item for item in items if item["cost"] <= self.coins]
        if not affordable:
            return None

        # Try to go for attack items first.
        attack_items = [item for item in affordable if item["type"] == "attack"]
        if attack_items:
            return max(attack_items, key=lambda x: x["value"]) 

        # If none, choose best healing item.
        heal_items = [item for item in affordable if item["type"] == "heal"]
        if heal_items:
            return max(heal_items, key=lambda x: x["value"])

        return random.choice(affordable)

def dice_roll():
    """
    Simulates a dice roll.

    Returns:
        int: A random integer from 1 to 6 representing the number rolled.

    Primary Author: Luis Jovel Lainez
    """
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
    """
    Displays the store items that a player can afford based on their coins.

    Args:
        coins (int): The number of coins the player currently has.

    Primary Author: Luis Jovel Lainez

    Techniques Claimed:
    - Usage of dictionaries
    """
    print("\n-- Store --")
    for item in STORE_ITEMS:
        if item["cost"] <= coins:
            sign = "+" if item["type"] == "heal" else "-"
            print(f"{item['name']} ({item['type']}, {sign}{item['value']}): {item['cost']} coins")

def get_store_choice(player):
    """
    Prompts the player to choose an item from the store.

    Args:
        player (Player): The player choosing the item.

    Returns:
        dict or None: The chosen store item if valid, otherwise None.

    Side Effects:
        May call input() or use the player's automatic selection logic.

    Primary Author: Luis Jovel Lainez

    Techniques Claimed:
    - Iteration
    """
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
    Manages the turn-based gameplay between two players, including rolling,
    store interactions, healing, attacking, and win conditions.

    Primary Author: Gerardo Sandoval  

    Techniques Claimed:
    - f-strings  
    - Conditional expressions 
    """

    def __init__(self, player1, player2):
        """
        Initializes the game with two players.

        Args:
            player1 (Player): The first player.
            player2 (Player): The second player.

        Primary Author: Gerardo Sandoval  
        """
        self.player1 = player1
        self.player2 = player2

    def get_opponent(self, current):
        """
        Gets the opponent of the current player.

        Args:
            current (Player): The player whose opponent is to be found.

        Returns:
            Player: The opposing player.

        Primary Author: Gerardo Sandoval  

        Techniques Claimed:
        - Conditional expression
        """
        return self.player2 if current == self.player1 else self.player1

    def play_turn(self, player):
        """
        Executes a player's turn: rolls the die, grants coins,
        lets the player buy and use an item, and applies its effects.

        Args:
            player (Player): The player taking the turn.

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
        Runs the game loop, alternating turns until one player is defeated.

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
    """
    Parses command-line arguments to get the human player's name.

    Returns:
        argparse.Namespace: Object containing the player's name.

    Primary Author: Tysen Wills  

    Techniques Claimed:
    - Use of argparse for command-line interface  
    - Handling required command-line input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, help="Enter your name")
    return parser.parse_args()

def main():
    """
    Initializes players and starts the game.

    Creates a human and computer player, then starts the turn-based game loop.

    Primary Author: Tysen Wills  
    """
    args = parse_args()
    player1 = Player(args.name, hp=100, max_hp=100, attack_power=0, heal_power=0)
    player2 = ComputerPlayer("Computer", hp=100, max_hp=100, attack_power=0, heal_power=0)
    game = Game(player1, player2)
    game.play()

if __name__ == "__main__":
    main()