from datetime import datetime, date

def get_user_birthdate():
    # Prompts the user for a birthdate and returns a valid date object
    while True:
        user_input = input("Enter your birthdate (YYYY-MM-DD): ") # Prompt user for their birthdate
        try:
            birth_date = datetime.strptime(user_input, "%Y-%m-%d").date() # Parse the input string into a date object
            if birth_date > date.today():
                print("❌ Birthdate cannot be in the future.") # Check if the birthdate is in the future
            else:
                return birth_date
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.") # Handle invalid date format

def calculate_age(birth_date):
    """Calculates age in years from the birth date."""
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

def get_week_day(some_date):
    """Returns the weekday name of the given date."""
    return some_date.strftime("%A") # Returns the full name of the weekday (e.g., "Monday", "Tuesday") by formatting the date object into a string

def main():
    birth_date = get_user_birthdate()
    age = calculate_age(birth_date)
    weekday = get_week_day(birth_date)
    print(f"You are {age} years old.") # Prints the user's age
    print(f"You were born on a {weekday}.") # Prints the day of the week the user was born
    print(f"Today is {get_week_day(date.today())}.") # Prints today's day of the week

if __name__ == "__main__":
    main()
