# Task 1: Date arithmetic - How Old Are You?
from datetime import datetime, date

def calculate_age(birthdate):
    today = date.today()
    # Calculate preliminary age
    age = today.year - birthdate.year
    # Adjust age if the birthday hasn't occurred yet this year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age

def main():
    user_input = input("Enter your birthdate (YYYY-MM-DD): ") # Prompt user for their birthdate
    try:
        birthdate = datetime.strptime(user_input, "%Y-%m-%d").date()
        if birthdate > date.today(): # Check if the birthdate is in the future
            print("Birthdate cannot be in the future.")
            return
        age = calculate_age(birthdate)
        print(f"You are {age} years old.") # Output the calculated age
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.") # Handle invalid date format

if __name__ == "__main__":
    main()