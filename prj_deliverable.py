# Luis Function
#Intended to facilitate the dice roll:
import random
def dice_roll():
    
    roll_one = random.randint(0, 6)
    roll_two = random.randint(0, 6)
    roll_three = random.randint(0, 6)
    roll_four = random.randint(0,6)
    total_roll = roll_one + roll_two
    player2_roll = roll_three + roll_four
    
    while (total_roll == player2_roll):
        
        
        if (total_roll != player2_roll):
            print(total_roll)
    
    
    print(total_roll)
    print(player2_roll)
    
dice_roll()
# Gerardo - Turn Function:
# Intended to swap turns after the player performs their move while keeping track of who went. 

def turn(p1_name, p2_name):
    starting_hp = 100
    damage = 10 # The damage is expected to change based on value of the roll, but
    # will stay at 10 for the purpose of the deliverable
    
    p1 = {"name": p1_name, "health": starting_hp}
    p2 = {"name": p2_name, "health": starting_hp}
    turn = 0
    players = [p1,p2]
    
    while p1["health"] > 0 and p2["health"] > 0:
        attacker = players[turn]
        defender = players[1-turn]
        defender["health"] -= damage
        print(f'{attacker["name"]} has just hit {defender["name"]} for {damage} damage')
        print(f'{defender["name"]} your health is now at {defender['health']}.')

        
        if defender["health"] <= 0:
            print(f'{attacker["name"]} has defeated {defender["name"]}.
                  {defender["name"]} better luck next time.')
            return f'{attacker["name"]} won the game'
        
        turn = 1-turn
# Tysen's - Computer player Function:
# Intended to be a really smart computer player to give the players competition.
def smart_computer(my_hp, my_max_hp, opp_hp, opp_max_hp, last_actions=None,
                                heal_range=(10, 20), attack_range=(8, 15)):
    if last_actions is None:
        last_actions = []
  #  Evaluate current state
    my_ratio = my_hp / my_max_hp
    opp_ratio = opp_hp / opp_max_hp
    hp_difference = my_hp - opp_hp

  # calculate expected scores
    expected_heal = sum(heal_range) / 2
    expected_attack = sum(attack_range) / 2

 # Determine if we can kill the opponent this turn
    can_kill = opp_hp <= attack_range[1]

 # Determine our risks
    at_risk = my_hp <= attack_range[1]

  # Enter panic mode if dangerously low
    in_panic_mode = my_hp < 0.2 * my_max_hp

  # risk profile 
    base_aggression = 0.5
    aggression_bonus = (my_ratio - opp_ratio) * 0.5  # scale from -0.5 to 0.5
    risk_tolerance = base_aggression + aggression_bonus

    # Clamp risk tolerance
    risk_tolerance = max(0.1, min(0.9, risk_tolerance))

    # Panic mode: prioritize healing, unless we can kill
    if in_panic_mode:
        if can_kill:
            return 'attack'
        else:
            return 'heal' if random.random() > 0.2 else 'attack'

    # If we are winning and can get a kill soon, attack
    if can_kill:
        return 'attack'

    # If opponent is a lot weaker be aggressive
    if hp_difference > 0.3 * my_max_hp and opp_hp > expected_attack:
        return 'attack'

    # Avoid over-healing or wasting heals
    if my_hp + heal_range[1] >= my_max_hp and opp_hp > my_hp:
        return 'attack'



    
