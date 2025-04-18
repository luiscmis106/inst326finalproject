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
