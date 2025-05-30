# 📌 A string is a sequence of characters enclosed in single ' or double " quotes
name = "John"

# ----------------------------------------
# 🔗 Basic String Operations
# ----------------------------------------

# 1.1 ➕ Concatenation (Joining Strings)
first = "John"
last = "Doe"
full = first + " " + last
print(full)  # Output: John Doe

# 1.2 ➕ Concatenation using f-string (recommended modern way)
another_full = f"{first} {last}"
print(another_full)  # Output: John Doe

# 2. 🔁 Repetition
laugh = "ha" * 3
print(laugh)  # Output: hahaha

# 3. 🔍 Indexing and Slicing (extracting parts of a string)
word = "Python"
print(word[0])      # Output: P (1st character)
print(word[-1])     # Output: n (last character)
print(word[1:4])    # Output: yth (2nd to 4th characters)
print(word[:3])     # Output: Pyt (1st to 3rd characters)
print(word[3:])     # Output: hon (4th to end)

# 4. 📏 Length of a String
word2 = "Apple"
word2_length = len(word2)
print(word2_length)  # Output: 5

# ----------------------------------------
# 🔧 String Methods (Useful built-in tools)
# ----------------------------------------

# 1. 🔠 Case Conversion
greeting = "hello world"

greeting_upper = greeting.upper()        # "HELLO WORLD"
greeting_lower = greeting_upper.lower()  # "hello world"
greeting_title = greeting_upper.title()  # "Hello World"
greeting_capitalize = greeting.capitalize()  # "Hello world"

print(greeting_upper)  # Output: HELLO WORLD

# 2. ✂️ Trimming Whitespace (removing spaces from the beginning/end)
not_clean_string = "  hello world  "
clean_string = not_clean_string.strip()        # 'hello world'
clean_left_string = not_clean_string.lstrip()  # 'hello world  '
clean_right_string = not_clean_string.rstrip() # '  hello world'

# 3. 🔎 Finding and 🔁 Replacing
message = "I love Python"
print(message.find("love"))              # Output: 2 (starts at index 2)
print(message.replace("love", "like"))   # Output: I like Python

# 4. 🍉 Splitting and 🧵 Joining
data = "apple,banana,cherry"
fruits = data.split(",")                 # ['apple', 'banana', 'cherry']
joined = "-".join(fruits)                # 'apple-banana-cherry'

print(fruits)
print(joined)

# 5. ✅ Checking Substrings
s = "Welcome to Python"
print("Python" in s)     # True
print("Java" not in s)   # True
