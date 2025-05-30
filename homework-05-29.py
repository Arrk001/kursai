birth_year = int(input("Enter your birth year: "))  # Input from user as an integer
birth_month = int(input("Enter your birth month: "))  # Input from user as an integer
birth_day = int(input("Enter your birth day: "))  # Input from user as an integer

# Automatically calculate the current date
from datetime import date # Getting the current date; importing date from datetime module
current_date = date.today() # Date today

# Calculating age
age = current_date.year - birth_year # Age is the difference between current year and birth year
if current_date.month < birth_month or (current_date.month == birth_month and current_date.day < birth_day): # Check if the birthday has occurred this year
    age -= 1  # -1 year, if the birthday hasn't occurred yet this year

print() # Blank line for better readability
print(f"You are {age} years old.")
print() # Blank line for better readability

# Creating categories based on age
if age <= 17 and age >= 0: # Age is between 0 and 17
    print("Age category: I.")
elif age <= 36 and age >= 18: # Age is between 18 and 36
    print("Age category: II.")
else :   # Age is 37 or older
    print("Age category: III.") 
print() # Blank line for better readability
