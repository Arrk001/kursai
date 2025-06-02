# Creating a grocery list
shopping_list = [] # Initializing an empty list to store grocery items
# Asking the user for input
while True:
    item = input("Enter an item to add to your grocery list (or type 'done' to finish): ") # Asking the user to enter items for the grocery list
    if item.lower() == 'done': # If the user types 'done', exit the loop
        break
    shopping_list.append(item) # Adding the item to the grocery list
# Displaying the final grocery list
print() # Blank line for better readability
print("Your grocery list:")
for item in shopping_list:
    print("- " + item)  
# Displaying the total number of items in the grocery list
print("Total number of items in your grocery list:", len(shopping_list))
print()  # Blank line for better readability

# List average calculator
numbers = [] # Initializing an empty list to store numbers
for i in range(5): # Loop to get 5 numbers from the user
    while True: # Loop to ensure valid input
        try:
            number = float(input(f"Enter number {i + 1} of 5: ")) # Asking the user to enter 5 numbers
            numbers.append(number) # Adding the number to the list
            break
        except ValueError: 
            print("Please enter a valid number.") # Asking the user for a valid number if input is not a number
# Displaying the average of the numbers
if numbers: # Ensure the list is not empty before calculating the average
    average = sum(numbers) / len(numbers) # Divide the sum of the numbers by the count of numbers
    print("The average of the numbers you entered is:", average)