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
                   heal_range=(10, 20), attack_range=(8, 15), num_iterations=2):
    if last_actions is None:
        last_actions = []

    # Initialize variables to store final decision
    final_action = None

    # Iterate through decision making multiple times
    for _ in range(num_iterations):
        # Evaluate current state
        my_ratio = my_hp / my_max_hp
        opp_ratio = opp_hp / opp_max_hp
        hp_difference = my_hp - opp_hp

        # calculate expected scores
        expected_heal = sum(heal_range) / 2
        expected_attack = sum(attack_range) / 2

        # checking if we can kill the opponent this turn
        can_kill = opp_hp <= attack_range[1]

        # determine our risks
        at_risk = my_hp <= attack_range[1]

        # enter panic mode if at risk of death
        in_panic_mode = my_hp < 0.2 * my_max_hp

        # risk assesment
        base_aggression = 0.5
        aggression_bonus = (my_ratio - opp_ratio) * 0.5  # scale from -0.5 to 0.5
        risk_tolerance = base_aggression + aggression_bonus

        #  risk tolerance
        risk_tolerance = max(0.1, min(0.9, risk_tolerance))

        # Panic mode: think healing first, unless we can kill
        if in_panic_mode:
            if can_kill:
                final_action = 'attack'
            else:
                final_action = 'heal' if random.random() > 0.2 else 'attack'

        # if we  winning and can get a kill soon, attack
        elif can_kill:
            final_action = 'attack'

        # if opponent is a lot weaker, be aggressive
        elif hp_difference > 0.3 * my_max_hp and opp_hp > expected_attack:
            final_action = 'attack'

        # avoid wasting heals
        elif my_hp + heal_range[1] >= my_max_hp and opp_hp > my_hp:
            final_action = 'attack'
        
        # random default to healing or attacking in case no decision is made
        if final_action is None:
            if random.random() < risk_tolerance:
                final_action = 'attack'
            else:
                final_action = 'heal'
        
        # Optionally, you can decide to stop iterating once an action has been chosen
        if final_action:
            break

    return final_action

# Guy's function
def player_turn(player, enemy, effects = None):
    if effects is None:
        effects = {}

    report = {}
    roll = random.randint(1, 20)

    # Decision logic based on player type and health 
    hp_ratio = player['hp'] / player['max_hp']
    
    if player['type'] == "healer" and hp_ratio < 0.5:
        action = "heal"
    elif player['type'] == "tank" and hp_ratio < 0.3:
        action = "heal"
    else:
        action = "attack"

    # Applies action
    if action == "attack":
        damage = roll + (5 if player['type'] == "warrior" else 0)
        enemy['hp'] = max(0, enemy['hp'] - damage)
        report['action'] = "attack"
        report['amount'] = damage
    else:  # heal
        heal = roll + (3 if player['type'] == "healer" else 0)
        player['hp'] = min(player['max_hp'], player['hp'] + heal)
        report['action'] = "heal"
        report['amount'] = heal

    # Update and return the turn summary
    report['player_hp'] = player['hp']
    report['enemy_hp'] = enemy['hp']
    report['effects'] = effects  # Could expand later with real logic

    return report
    
