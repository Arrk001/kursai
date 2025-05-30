# 📚 Python Lists - Real-World Examples and Operations

# ----------------------------------------
# 🧺 1. Creating a List
# ----------------------------------------

fruits = ["apple", "banana", "cherry"]
print("🍎 Initial list of fruits:", fruits)

# ----------------------------------------
# ➕ 2. Adding Items
# ----------------------------------------

fruits.append("orange")  # Add to end
print("Added 'orange':", fruits)

fruits.insert(1, "mango")  # Insert at position 1
print("Inserted 'mango' at index 1:", fruits)

# ----------------------------------------
# ➖ 3. Removing Items
# ----------------------------------------

fruits.remove("banana")  # Remove by value
print("Removed 'banana':", fruits)

popped = fruits.pop()    # Remove last item
print(f"Popped item: {popped}")
print("After pop:", fruits)

# ----------------------------------------
# 🔍 4. Accessing Items
# ----------------------------------------

print("First fruit:", fruits[0])
print("Last fruit:", fruits[-1])

# ----------------------------------------
# 🔁 5. Looping Through a List
# ----------------------------------------

print("🍓 All fruits in the list:")
for fruit in fruits:
    print("-", fruit)

# ----------------------------------------
# 🔢 6. List Length
# ----------------------------------------

print("Total number of fruits:", len(fruits))

# ----------------------------------------
# 🧮 7. List of Numbers
# ----------------------------------------

numbers = [5, 3, 8, 6]
print("🔢 Numbers:", numbers)

print("Max:", max(numbers))
print("Min:", min(numbers))
print("Sum:", sum(numbers))

# ----------------------------------------
# 🧼 8. Sorting and Reversing
# ----------------------------------------

numbers.sort()
print("Sorted numbers:", numbers)

numbers.reverse()
print("Reversed numbers:", numbers)

# ----------------------------------------
# 🧱 9. List Slicing
# ----------------------------------------

print("First two numbers:", numbers[:2])
print("Last two numbers:", numbers[-2:])

# ----------------------------------------
# 🧬 10. Copying a List
# ----------------------------------------

copied_fruits = fruits.copy()
print("Copied fruits:", copied_fruits)

# ----------------------------------------
# 🔄 11. List Comprehension
# ----------------------------------------

squared = [x**2 for x in numbers]
print("Squared numbers:", squared)

# ----------------------------------------
# 🧪 12. Check for Item
# ----------------------------------------

if "apple" in fruits:
    print("✅ Apple is in the list.")

if "banana" not in fruits:
    print("❌ Banana is not in the list.")
