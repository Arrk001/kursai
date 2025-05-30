print("Hello, World!");
print("Goodbye, World!");
print("Welcome!")
print("Looks like this works!")
name = "Lukas" # String variable
age = 29 # Integer variable
height = 1.81 # Float variable
is_married = True # Boolean variable
is_turtle = False # Boolean variable
time = input("What time is it right now in hours? ") # Input from user
is_old_enough = age >= 18 # Boolean expression
print()  # Blank line
if is_old_enough: # Will be printed ONLY if age is 18 or older
    print("I am old enough.")
elif height >= 1.8: # Will be printed ONLY if age is less than 18 but height is greater than 1.8
    print("I am tall enough, but not old enough.")
else: # Will be printed ONLY if both age is less than 18 and height is less than 1.8
    print("I am not old enough or tall enough.")
print()  # Blank line
print(f"My name is {name} and I am {age} years old.")
print(f"My height is {height} meters.")
print(f"Am I married? {'Yes' if is_married else 'No'}")
print(f"Am I a turtle? {'Yes' if is_turtle else 'No'}")
print(f"Am I old enough? {'I guess so, yes' if is_old_enough else 'No'}")
time = int(time) # Convert input to integer 
print()  # Blank line
if time < 20:
    print("The lesson is still going.")
elif time >= 20:
    print("The lesson should have ended.")


print()  # Blank line
# lists
list = ['kiwi', 'peach', 'banana', 'potato']

print(f"List: {list[1]}") # Specific item in list
print(f"List: {list[0]}") # First item is always 0
print(f"List: {list[-1]}") # Last item is always -1
print(f"List: {list[1:3]}") # Items from index 1 to 2 (3 is not included)
print(f"Length of string: {len(' 1')}") # Length of string characters
print(f"Length of list: {len(list)}") # Length of list items
print() # Blank line