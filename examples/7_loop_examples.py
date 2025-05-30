# 🔁 Python Loop Examples
# This file demonstrates how to use for-loops and while-loops in real-world situations.

# ----------------------------------------
# 🔢 1. For Loop with a Range
# ----------------------------------------

print("🔁 Counting from 1 to 5:")
for i in range(1, 6):
    print(i)

# ----------------------------------------
# 🧺 2. For Loop Through a List
# ----------------------------------------

fruits = ["apple", "banana", "cherry"]

print("🍓 Fruits in the basket:")
for fruit in fruits:
    print("-", fruit)

# ----------------------------------------
# 🔁 3. While Loop Example
# ----------------------------------------

print("⏳ Counting down from 5:")
count = 5
while count > 0:
    print(count)
    count -= 1
print("🚀 Lift off!")

# ----------------------------------------
# 🧠 4. Loop with User Input
# ----------------------------------------

print("🎮 Enter your favorite movies (type 'done' to finish):")
movies = []

while True:
    movie = input("Movie: ")
    if movie.lower() == "done":
        break
    movies.append(movie)

print("🎬 Your movies:", movies)

# ----------------------------------------
# 🎯 5. Loop With Condition (Even Numbers)
# ----------------------------------------

print("✅ Even numbers from 1 to 10:")
for num in range(1, 11):
    if num % 2 == 0:
        print(num)

# ----------------------------------------
# ❌ 6. Using Continue and Break
# ----------------------------------------

print("🛑 Loop that skips 3 and stops at 7:")
for i in range(1, 10):
    if i == 3:
        continue  # Skip 3
    if i == 7:
        break     # Stop loop at 7
    print(i)

# ----------------------------------------
# 🔄 7. Nested Loops
# ----------------------------------------

print("📅 Multiplication Table (1–3):")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}")
    print("---")
