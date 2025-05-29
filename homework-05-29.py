user_bd_year = int(input("Enter your birth year: "))  # Input from user as an integer
user_bd_month = int(input("Enter your birth month: "))  # Input from user as an integer
user_bd_day = int(input("Enter your birth day: "))  # Input from user as an integer



from datetime import datetime 
from dateutil.relativedelta import relativedelta

birth_date = datetime(user_bd_year, user_bd_month, user_bd_day) # Create a datetime object for the birth date

today = datetime.now()


difference = relativedelta(today, birth_date)


# Get age in years
age_in_years = difference.years

print()# Print the user's age in years, months, and days
print(f"You are {difference.years} years old.")
