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
