def parse_price_list(user_input):
    prices_list_str = user_input.split(",")
    prices_list = []

    for price in prices_list_str:
        float_price = float(price)
        prices_list.append(float_price)

    return prices_list


# 1. prompt user input: "Enter item prices separated by commas"

user_input = input("Enter item prices separated by commas: ")
price_list = parse_price_list(user_input)

# 2. write a function that sums item prices to a float variable

sum_of_prices = sum(price_list)

# 3. get how many items are in the list of shopping cart.

items_count = len(price_list)

# 4. count item average price for the shopping cart 

average = sum_of_prices / items_count

# 5. write an algorithm that counts how many items cost more than 10$

how_many_items_expensive = sum(1 for x in price_list if x > 10)

print(f"Total: {sum_of_prices}\nAverage: {round(average, 2)}\nItems over $10: {how_many_items_expensive}")
