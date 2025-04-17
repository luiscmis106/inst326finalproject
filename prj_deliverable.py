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
        
    
