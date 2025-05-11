import sys
import random
from argparse import ArgumentParser

class Player:
    def __init__(self, name, health, max_health, attack_power=0, heal_power=0, type="warrior"):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.attack_power = attack_power
        self.heal_power = heal_power
        self.type = type
        self.coins = 0

    def is_alive(self):
        return self.health > 0

    def attack(self, coins_spent):
        return coins_spent * self.attack_power

    def heal(self, coins_spent):
        heal_amount = coins_spent * self.heal_power
        self.health = min(self.max_health, self.health + heal_amount)
        return heal_amount




class ComputerPlayer(Player):
    """
    A subclass of Player that represents a computer-controlled player in the game. 
    The computer player makes decisions based on its health, attack power, and healing 
    power, as well as the state of the opponent's health.

    Attributes:
        hp (int): Current health of the computer player.
        max_hp (int): Maximum health of the computer player.
        attack_power (int): The attack power of the computer player.
        heal_power (int): The healing power of the computer player.
        type (str): The type of the player (not directly used in ComputerPlayer, but inherited from Player).
    
    Methods:
        __init__(self, name, hp, max_hp, attack_power=0, heal_power=0):
            Initializes a ComputerPlayer instance with the given attributes.
        
        choose_action(self, opponent, panic_threshold=0.2):
            Determines the next action the computer player should take based on its own state 
            and the state of the opponent. The decision-making considers panic, the ability to 
            kill, and healing needs.
    """

    def __init__(self, name, hp, max_hp, attack_power=0, heal_power=0):
        """
        Initializes a new ComputerPlayer object with the given attributes.
        
        Args:
            name (str): The name of the computer player.
            hp (int): The current health of the computer player.
            max_hp (int): The maximum health of the computer player.
            attack_power (int, optional): The attack power of the computer player. Defaults to 0.
            heal_power (int, optional): The healing power of the computer player. Defaults to 0.
        """
    def __init__(self,name, hp, max_hp, attack_power=0, heal_power=0):
        super().__init__(hp,name, max_hp, attack_power, heal_power)

    def choose_action(self, opponent, panic_threshold=0.2,):
       """
        Determines the action the computer player should take on its turn.

        The decision-making logic considers:
        - If the computer playerneeds to go into panic mode (health is below a certain threshold), 
          it will try to heal if possible.
        - If the computer player is able to win with its attack, it will choose to attack.
        - If the computer player needs to be healed, it will prioritize healing.
        - Otherwise, it chooses the best action (either attack or heal) based on available power.
        
        Args:
            opponent (Player): The opponent player object that the computer player faces.
            panic_threshold (float, optional): The health threshold for panic mode (as a fraction of max health). Defaults to 0.2.

        Returns:
            str: The action the computer player will take. Can be either "attack" or "heal".
        """
        my_hp, my_max, atk, heal = self.hp, self.max_hp, self.attack_power, self.heal_power
        opp_hp = opponent.hp

        in_panic = my_hp < panic_threshold * my_max
        can_kill = atk > 0 and opp_hp <= atk
        can_heal = heal > 0 and my_hp < my_max
        needs_heal = my_hp < opp_hp and heal > 0

        # Score actions using lambda as key function
        actions = {
            "attack": atk if atk > 0 else -1,
            "heal": heal if can_heal else -1
        }

        decision = (
            "heal" if in_panic and can_heal else
            "attack" if can_kill else
            "heal" if needs_heal else
            max(actions.items(), key=lambda pair: pair[1])[0]
        )

        return decision

class Game:
    def __init__(self, *players):
        self.players = list(players)
        self.current_turn = 0

    def play_turn(self, player, coins_to_use, action="auto"):
        if not player.is_alive():
            return
        chosen_action = (
            action if action in {"attack", "heal"}
            else ("heal" if player.health < 30 else "attack")
        )
        coins_spent = min(coins_to_use, player.coins)

        with open("game_log.txt", "a") as log:
            log.write(f"{player.name} used {coins_spent} coins to {chosen_action}\n")

        if chosen_action == "attack":
            target = self.get_opponent(player)
            if target:
                damage = player.attack(coins_spent)
                target.health -= damage
                print(f"{player.name} attacked {target.name} for {damage} damage!")
        else:
            player.heal(coins_spent)
            print(f"{player.name} healed for {coins_spent * 3} health!")

        print(f"{player.name} → Health: {player.health}, Coins: {player.coins}")

    def get_opponent(self, player):
        return next(p for p in self.players if p != player)

    def is_game_over(self):
        return any(not p.is_alive() for p in self.players)

    def get_winner(self):
        alive = [p for p in self.players if p.is_alive()]
        return alive[0] if alive else None

    def end_game(self):
        winner = self.get_winner()
        loser = next((p for p in self.players if p != winner), None)

        print("\n--- Game Over ---")
        if winner:
            print(f" Winner: {winner.name} with {winner.health} health remaining!")
            print(f" Eliminated: {loser.name}")
        else:
            print("It's a draw. Both players were eliminated.")
def parse_args(arglist):
    """
    Parse command-line arguments for the game.

    Required arguments:
        - name- the name of the player
        - hp- starting health points
        - max_hp- maximum health points

    Args:
        arglist (list of str): arguments from the command line.

    Returns:
        namespace: the parsed arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("name", help="player's name")
    parser.add_argument("hp", type=int, help="starting health")
    parser.add_argument("max_hp", type=int, help="maximum health")
    return parser.parse_args(arglist)

def main(args):
       """
    Main function to control the flow of the game. It initializes the player and enemy, 
    handles store purchases (if specified), and controls the game loop. 


    Args:
        args (namespace): The arguments parsed from the command line. These arguments include:
            - name: The name of the player.
            - hp: The starting health of the player.
            - max_hp: The maximum health of the player.
    Returns:
        None
    """
    player = Player(name=args.name, hp=args.hp, max_hp=args.max_hp, attack_power=0, heal_power=0, type="none")
    player.coins = random.randint(1, 6)
    print(f"{player.name} rolled and got {player.coins} coins!")

    # Store purchase before the battle if argument provided
    if args.store_first:
        store(player)
        if player.attack_power == 0 and player.heal_power == 0:
            print("You need to purchase a class to start the game.")
            return
            
    enemy = ComputerPlayer(name="EnemyBot", hp=40, max_hp=40, attack_power=0, heal_power=0)
    game = Game(player, enemy)

    
    while not game.is_game_over():
        print(f"\n{player.name}'s Turn")
        game.play_turn(player, coins_to_use=5)

        if enemy.is_alive():
            action = enemy.choose_action(player)
            print(f"{enemy.name} chooses to {action}.")
            if action == "attack":
                player.hp = max(0, player.hp - enemy.attack_power)
                print(f"{enemy.name} dealt {enemy.attack_power} damage.")
            elif action == "heal":
                enemy.hp = min(enemy.max_hp, enemy.hp + enemy.heal_power)
                print(f"{enemy.name} healed for {enemy.heal_power} HP.")

    game.end_game()
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)
