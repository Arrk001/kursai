from .models import ItemModel
from rich import print

PATH_TO_DB = "C:/Users/lukas/Desktop/kursai/fastapi_demo/product_database.csv"

def collect_starting_data():
    with open(PATH_TO_DB, "r", encoding="utf-8-sig") as f:
        products_csv = f.read()

    products_str_list = products_csv.strip().split("\n")

    product_list: list[ItemModel] = []
    for i, product_str in enumerate(products_str_list):
        if i == 0:
            continue  # skip the header row
        if not product_str.strip():
            continue  # skip empty lines

        product_parts = product_str.split(",")
        product = ItemModel(
            name=product_parts[0],
            price=float(product_parts[1]),
            weight=float(product_parts[2]),
            quantity_in_stock=int(product_parts[3]),
            itemid=int(product_parts[4])
        )
        product_list.append(product)

    return product_list
