# Chapter 4, Lesson 1 - Scope
# Find the bug in the code on line 13. We're using variable names from the wrong scope. Fix it!

def get_max_health(modifier, level):
    return modifier * level


my_modifier = 5
my_level = 10

## don't touch above this line

max_health = get_max_health(my_modifier, my_level) # This line was using "modifier" and "level" instead of "my_modifier" and "my_level"

# don't touch below this line

print(f"max_health is: {max_health}")
# This code defines a function to calculate the maximum health based on a modifier and level.

# Chapter 4, Lesson 2 - Global Scope
# Let's change how we are calculating our player's stats! The only thing we should need to define globally is the character level and then let our functions do the rest!
# Declare the variable player_level at the top of the global scope and set it to 4.

player_level = 4  # Global variable for player level

# Don't touch below this line


def calculate_health(modifier):
    return player_level * modifier


def calculate_primary_stats(armor_bonus, modifier):
    return armor_bonus + modifier + player_level


print(f"Character has {calculate_health(10)} max health.")

print(f"Character has {calculate_primary_stats(3, 8)} primary stats.")