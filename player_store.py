import dice_roll
class player_store:
    """This is the store where a player can buy powerups based on an odd
    numbered dice roll"""
    power_up = {3: "Skip turn", 
                 5: "Deal 2 extra damage",
                 7: "Block next attack",
                 9: "Heal 2 HP",
                 11: "Shield 2 damage",
                 13: "Opponent always misses",
                 15: "Repel next attack",
                 17: "Take 3 HP from opponent",
                 19: "Player always hits"}
    
    if dice_roll.random == 0:
        print("You don't have enough points!")
    else:
        print("Welcome to the store! What would you like to purchase?")
        
    if dice_roll.random == power_up.get(3):
        print("Would you like to buy the ability to skip one turn?")
    elif dice_roll.random == power_up.get(5):
        print("Would you like for your next attack to deal 2 additional damage")
    elif dice_roll.random == power_up.get(7):
        print("Would you like to block the next attack?")
    elif dice_roll.random == power_up.get(9):
        print("Would you like to instantly restore 2 HP?")
    elif dice_roll.random == power_up.get(11):
        print("Would you like to shield the next 2 damage points?")
    elif dice_roll.random == power_up.get(13):
        print("Would you like for your opponent to miss their next action?")
    elif dice_roll.random == power_up.get(15):
        print("Would you like to deflect the next attack to your enemy?")
    elif dice_roll.random == power_up.get(17):
        print("Would you like to drain 3 HP from your enemy?")
    elif dice_roll.random == power_up.get(19):
        print("Would you like to attack regardless of your dice roll?")