# 🧱 Python Data Types
# This script introduces common Python data types with real-world examples.

# ----------------------------------------
# 🔤 1. String (text)
# ----------------------------------------

name = "Alice"
city = "Vilnius"
greeting = f"Hello, {name} from {city}!"

print(greeting)  # Output: Hello, Alice from Vilnius!

# ----------------------------------------
# 🔢 2. Integer (whole number)
# ----------------------------------------

age = 25
apples = 10
total_apples = apples + 5

print(f"🍎 Total apples: {total_apples}")  # 15

# ----------------------------------------
# 🔣 3. Float (decimal number)
# ----------------------------------------

temperature = 23.5
price = 19.99
average_score = 87.4

print(f"🌡️ Today's temperature is {temperature}°C")

# ----------------------------------------
# ✅ 4. Boolean (True or False)
# ----------------------------------------

is_sunny = True
is_raining = False

if is_sunny and not is_raining:
    print("😎 It's a great day to go outside!")
else:
    print("☔ Stay indoors today.")

# ----------------------------------------
# 📦 5. List (ordered collection)
# ----------------------------------------

fruits = ["apple", "banana", "cherry"]
print(f"🍇 Favorite fruits: {fruits}")
print(f"My favorite is: {fruits[0]}")  # apple

# Add an item
fruits.append("orange")
print(f"Updated list: {fruits}")

# ----------------------------------------
# 📚 6. Tuple (ordered, unchangeable collection)
# ----------------------------------------

dimensions = (1920, 1080)
print(f"📺 Screen resolution: {dimensions[0]}x{dimensions[1]}")

# ----------------------------------------
# 🗃️ 7. Dictionary (key-value pairs)
# ----------------------------------------

person = {
    "name": "Alice",
    "age": 25,
    "city": "Vilnius"
}

print(f"👩 {person['name']} lives in {person['city']}.")

# Add a new key-value pair
person["hobby"] = "painting"
print(person)

# ----------------------------------------
# 🧩 8. Set (unordered, unique items)
# ----------------------------------------

unique_numbers = {1, 2, 2, 3, 4}
print(f"🎲 Unique numbers: {unique_numbers}")  # {1, 2, 3, 4}

# Add new item
unique_numbers.add(5)
print(unique_numbers)

# ----------------------------------------
# 🧪 9. Type Checking
# ----------------------------------------

print(type(name))         # <class 'str'>
print(type(age))          # <class 'int'>
print(type(temperature))  # <class 'float'>
print(type(is_sunny))     # <class 'bool'>
print(type(fruits))       # <class 'list'>
print(type(dimensions))   # <class 'tuple'>
print(type(person))       # <class 'dict'>
print(type(unique_numbers))  # <class 'set'>
