# Homework: Convert temperature from Celsius to Fahrenheit
celsius = int(input("Enter temperature in Celsius: "))  # Input temperature in Celsius
fahrenheit = (celsius * 9/5) + 32  # Convert Celsius to Fahrenheit
print(f"Temperature in Fahrenheit: {fahrenheit}")  # Output the result (Celsius to Fahrenheit)
print() # Blank line for better readability

# Homework: Convert temperature from Fahrenheit to Celsius
fahrenheit = int(input("Enter temperature in Fahrenheit: ")) # Input temperature in Fahrenheit
celsius = (fahrenheit - 32) * 5/9  # Convert Fahrenheit to Celsius
print(f"Temperature in Celsius: {celsius}")  # Output the result (Fahrenheit to Celsius)
print()  # Blank line for better readability

# Homework: Calculate BMI (Body Mass Index)
weight = float(input("Enter your weight in kg: ")) # Input weight in kilograms
height = float(input("Enter your height in meters: ")) # Input height in meters
print()  # Blank line for better readability
bmi = weight / (height ** 2)  # Calculate BMI
print(f"Your BMI is: {bmi}")  # Output the result (BMI)
print()  # Blank line for better readability

# Creating categories based on BMI
if bmi < 18.5 : # BMI is less than 18.5
    print("BMI category: Underweight.")
elif bmi >= 18.6 and bmi <= 24.9: # BMI is between 18.6 and 24.9
    print("BMI category: Healthy Weight.")
elif bmi >= 25 and bmi <= 29.9: # BMI is between 25 and 29.9
    print("BMI category: Overweight.")
elif bmi >= 30:  # BMI is 30 or greater
    print("BMI category: Obesity.")
print() # Blank line for better readability