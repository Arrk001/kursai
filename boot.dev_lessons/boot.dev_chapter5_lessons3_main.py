# Complete the take_magic_damage function. It should return the new health after calculating how much magic-type damage the player takes. Here is a description of the arguments:
# health: The player's starting health
# resist: The player's magic resistance. This reduces the damage they take by a static amount
# amp: The attacker's magic amplification. This increases the damage they deal by a multiplier
# spell_power: The base damage of the spell
# First, calculate the total maximum damage to be inflicted by multiplying the spell_power by the amp. Then, subtract the 
# resist from the total damage to get the actual damage dealt. Apply that damage to the player's health and return the new health.

def take_magic_damage(health, resist, amp, spell_power):
    max_damage = spell_power * amp
    actual_damage = max_damage - resist
    final_health = health - actual_damage
    return final_health
