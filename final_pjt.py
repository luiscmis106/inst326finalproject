#updated computer ngl idk 
class ComputerPlayer(Player):
    def __init__(self, hp, max_hp, attack_power=0, heal_power=0):
        super().__init__(hp, max_hp, attack_power, heal_power)

    def choose_action(self, opponent, panic_threshold=0.2,):
        # Sequence unpacking for readability
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