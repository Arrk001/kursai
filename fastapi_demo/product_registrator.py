# product_registrator.py
import csv
from .models import ItemModel

PATH_TO_DB = "C:/Users/lukas/Desktop/kursai/fastapi_demo/product_database.csv"

def save_product_to_file(item: ItemModel):
    """Appends a new product to the CSV file."""
    with open(PATH_TO_DB, "a", encoding="utf-8-sig", newline='') as f:
        writer = csv.writer(f)
        # Check if the file is empty to write header, though collect_starting_data might handle initial header
        # For simplicity, we'll assume header is always there.
        writer.writerow([item.name, item.price, item.weight, item.quantity_in_stock, item.itemid])

def write_all_products_to_file(products_list: list[ItemModel]):
    """Rewrites the entire list of products to the CSV file."""
    # The 'w' mode truncates the file, effectively clearing it before writing
    with open(PATH_TO_DB, "w", encoding="utf-8-sig", newline='') as f:
        writer = csv.writer(f)
        # Write the header row first
        writer.writerow(["Product Name", "Price", "Weight", "Number of Items", "Item ID"])
        # Write each product from the current in-memory list
        for product in products_list:
            writer.writerow([
                product.name,
                product.price,
                product.weight,
                product.quantity_in_stock,
                product.itemid
            ])