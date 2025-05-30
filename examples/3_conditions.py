# ✅ Python Conditionals (if/elif/else)
# This file uses real-world examples to show how decision-making works in Python.

# ----------------------------------------
# 🧒 1. Age Checker
# ----------------------------------------

age = 18

if age >= 18:
    print("🔓 You can vote!")
else:
    print("🔒 You are too young to vote.")

# ----------------------------------------
# 🍕 2. Pizza Order Size
# ----------------------------------------

pizza_size = "large"

if pizza_size == "small":
    print("🍕 Small pizza costs $8.")
elif pizza_size == "medium":
    print("🍕 Medium pizza costs $10.")
elif pizza_size == "large":
    print("🍕 Large pizza costs $12.")
else:
    print("❓ Size not recognized.")

# ----------------------------------------
# 📚 3. Pass or Fail Grade
# ----------------------------------------

grade = 72

if grade >= 90:
    print("🏅 Grade: A")
elif grade >= 80:
    print("🎖️ Grade: B")
elif grade >= 70:
    print("👍 Grade: C")
elif grade >= 60:
    print("⚠️ Grade: D")
else:
    print("❌ Grade: F")

# ----------------------------------------
# 🚘 4. Speed Limit Warning
# ----------------------------------------

speed = 85
limit = 70

if speed > limit:
    print("🚨 You are speeding!")
else:
    print("✅ You are within the speed limit.")

# ----------------------------------------
# 💵 5. ATM Balance Check
# ----------------------------------------

balance = 100
withdraw = 80

if withdraw <= balance:
    print(f"💰 Withdrawal successful. New balance: ${balance - withdraw}")
else:
    print("❌ Insufficient funds.")

# ----------------------------------------
# 🧾 6. Discount Eligibility
# ----------------------------------------

is_student = True
is_senior = False

if is_student or is_senior:
    print("🎉 You get a 10% discount!")
else:
    print("💳 No discount available.")

# ----------------------------------------
# 📦 7. Nested Conditions: Online Order
# ----------------------------------------

in_stock = True
has_credit_card = True

if in_stock:
    if has_credit_card:
        print("🛒 Order placed successfully.")
    else:
        print("💳 Please add a payment method.")
else:
    print("❌ Item is out of stock.")

# ----------------------------------------
# 🎲 8. Even or Odd Checker
# ----------------------------------------

number = 11

if number % 2 == 0:
    print(f"{number} is an 🟰 even number.")
else:
    print(f"{number} is an ➗ odd number.")

# ----------------------------------------
# 🏃‍♂️ 9. Race Participation
# ----------------------------------------

is_registered = True
is_healthy = True

if is_registered and is_healthy:
    print("🏁 You're ready to join the race!")
else:
    print("🛑 You can't participate.")