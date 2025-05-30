# ➗ Python Math Operations
# This script covers basic and advanced math operations in Python.

# ----------------------------------------
# ➕➖✖️➗ 1. Basic Arithmetic Operators
# ----------------------------------------

a = 10
b = 3

print(a + b)   # ➕ Addition: 13
print(a - b)   # ➖ Subtraction: 7
print(a * b)   # ✖️ Multiplication: 30
print(a / b)   # ➗ Division: 3.333...

# ----------------------------------------
# ⚙️ 2. Integer Division and Modulo
# ----------------------------------------

print(a // b)  # 🧮 Floor Division: 3 (truncates decimal)
print(a % b)   # 🧩 Modulo: 1 (remainder of division)

# ----------------------------------------
# 🎯 3. Exponentiation
# ----------------------------------------

print(2 ** 3)   # 2³ = 8
print(pow(4, 2))  # Alternative: 4² = 16

# ----------------------------------------
# 🧠 4. Using the math Module (Advanced Math)
# ----------------------------------------

import math

# 🔢 Constants
print(math.pi)        # 3.141592653...
print(math.e)         # 2.718281828...

# 🧮 Roots and Powers
print(math.sqrt(16))  # √16 = 4.0
print(math.pow(2, 5)) # 2⁵ = 32.0

# 🧾 Logarithms
print(math.log(100, 10))  # log base 10: 2.0
print(math.log2(8))       # log base 2: 3.0
print(math.log10(1000))   # log base 10: 3.0

# 🧊 Rounding and Truncation
print(math.floor(3.7))    # 3
print(math.ceil(3.1))     # 4
print(math.trunc(3.9))    # 3

# 📐 Trigonometry (angles in radians)
angle = math.radians(30)
print(math.sin(angle))    # sin(30°) ≈ 0.5
print(math.cos(angle))    # cos(30°)
print(math.tan(angle))    # tan(30°)

# ----------------------------------------
# 🎲 5. Random Numbers
# ----------------------------------------

import random

print(random.randint(1, 6))        # Random int between 1 and 6 (inclusive)
print(random.random())             # Random float between 0.0 and 1.0
print(random.uniform(1, 10))       # Random float between 1 and 10
print(random.choice(['apple', 'banana', 'cherry']))  # Random choice from a list

# ----------------------------------------
# 📏 6. Absolute and Rounding Functions
# ----------------------------------------

print(abs(-20))         # ➕ Absolute value: 20
print(round(3.14159, 2))  # 🎯 Round to 2 decimals: 3.14

# ----------------------------------------
# 🧪 7. Type Casting Reminder
# ----------------------------------------

x = 5
y = 2
print(float(x) / y)     # Make sure to use float for accurate division: 2.5
