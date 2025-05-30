# 📦 Python Conversion Operations
# This script demonstrates how to convert between different data types in Python.

# ----------------------------------------
# 🔁 Type Conversion Basics
# ----------------------------------------

# 1️⃣ int() - Convert to Integer
print(int("42"))        # From string: '42' -> 42
print(int(3.7))         # From float: 3.7 -> 3 (truncates decimals)

# 2️⃣ float() - Convert to Float
print(float("3.14"))    # From string: '3.14' -> 3.14
print(float(10))        # From int: 10 -> 10.0

# 3️⃣ str() - Convert to String
print(str(123))         # From int: 123 -> "123"
print(str(4.56))        # From float: 4.56 -> "4.56"

# 4️⃣ bool() - Convert to Boolean
print(bool(0))          # False (zero is false)
print(bool(1))          # True
print(bool(""))         # False (empty string is false)
print(bool("Python"))   # True (non-empty string is true)

# ----------------------------------------
# 🔄 Conversions Between Data Structures
# ----------------------------------------

# 5️⃣ list() - Convert to List
print(list("hello"))           # ['h', 'e', 'l', 'l', 'o']
print(list((1, 2, 3)))         # [1, 2, 3]

# 6️⃣ tuple() - Convert to Tuple
print(tuple("abc"))           # ('a', 'b', 'c')
print(tuple([4, 5, 6]))       # (4, 5, 6)

# 7️⃣ set() - Convert to Set (removes duplicates)
print(set([1, 2, 2, 3]))      # {1, 2, 3}
print(set("banana"))         # {'a', 'n', 'b'}

# 8️⃣ dict() - Convert to Dictionary
# Only works with valid structures like lists of pairs
pairs = [("name", "John"), ("age", 30)]
print(dict(pairs))           # {'name': 'John', 'age': 30}

# ----------------------------------------
# 📐 Numeric Conversions and Formatting
# ----------------------------------------

# 9️⃣ round() - Rounding Numbers
print(round(3.14159, 2))     # 3.14
print(round(5.678))          # 6 (default: nearest integer)

# 🔟 int() with base - Convert from binary, hex, etc.
binary_str = "1010"
hex_str = "1F"
print(int(binary_str, 2))    # 10 (binary to decimal)
print(int(hex_str, 16))      # 31 (hexadecimal to decimal)

# ----------------------------------------
# 🧪 Type Checking (Optional for debugging)
# ----------------------------------------

x = 42
print(type(x))               # <class 'int'>
y = "Python"
print(type(y))               # <class 'str'>
z = [1, 2, 3]
print(type(z))               # <class 'list'>
