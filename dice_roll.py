import random
def dice_roll():
    """The dice roll for the game
    
    Returns:
        The plyer's dice roll and the opponent's dice roll
    """
    
    roll_one = random.randint(0, 6)
    roll_two = random.randint(0, 6)
    roll_three = random.randint(0, 6)
    roll_four = random.randint(0,6)
    total_roll = roll_one + roll_two
    player2_roll = roll_three + roll_four
    
    power = {0: "Skip turn", 
                 2: "Deal 2 extra damage",
                 4: "Heal 2 HP",
                 6: "Shield 2 damage",
                 8: "Opponent skips turn",
                 10: "Repel next attack",
                 12: "Take 3 HP from opponent"}
    
    if(total_roll == 0 or player2_roll == 0):
        power.get(0)
    elif (total_roll == 2 or player2_roll == 2):
        power.get(2)
    elif(total_roll == 4 or player2_roll == 4):
        power.get(4)
    elif(total_roll == 6 or player2_roll == 6):
        power.get(6)
    elif(total_roll == 8 or player2_roll == 8):
        power.get(8)
    elif(total_roll == 10 or player2_roll == 10):
        power.get(10)
    elif(total_roll == 12 or player2_roll == 12):
        power.get(12)
    
    
    if (total_roll != player2_roll):
        return(total_roll, player2_roll)
    
    while (total_roll == player2_roll):
        break
    return("Same number, roll again!")
    
    
dice_roll()