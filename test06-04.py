# Prompt for price input and validate
def get_price():
    """Prompts the user for a price and returns a valid float."""
    while True:
        user_input = input("Enter the price of the item: ")
        try:
            price = float(user_input)
            if price < 0:
                print("Price cannot be negative.")
            else:
                return price
        except ValueError:
            print("Invalid price format. Please enter a valid number.")

# Adding up all the prices  
def calculate_total(prices):
    """Calculates the total price from a list of prices."""
    return sum(prices)

# Average price calculation
def calculate_average(prices):
    """Calculates the average price from a list of prices."""
    if not prices:
        return 0
    return sum(prices) / len(prices)

# Items in list costing over 10
def filter_expensive_items(prices):
    """Filters and returns items costing over 10."""
    return [price for price in prices if price > 10]

def main():
    prices = []
    while True:
        price = get_price()
        prices.append(price)
        more = input("Add another item? (yes/no): ")
        if more.lower() != "yes":
            break

    total_price = calculate_total(prices)
    average_price = calculate_average(prices)
    expensive_items = filter_expensive_items(prices)

    print("Total price:", total_price)
    print("Average price:", average_price)
    print("Items costing over 10:", expensive_items)

# 🔽 This makes your code run when executed
if __name__ == "__main__":
    main()