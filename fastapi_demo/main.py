# main.py
from fastapi import FastAPI, HTTPException
from typing import Optional # <--- Add this import for Optional
from .models import ItemModel, ItemUpdateModel # <--- Import the new ItemUpdateModel
from .initializer import collect_starting_data
from .product_registrator import save_product_to_file, write_all_products_to_file
import csv

app = FastAPI()

PATH_TO_DB = "C:/Users/lukas/Desktop/kursai/fastapi_demo/product_database.csv"

# RAM atmintis (Labai laikina)
products: list[ItemModel] = collect_starting_data()


@app.get("/")
def initial():
    return "Labas Pasauli :), čia yra mano pirmas FastAPI projektas! Prašome eiti į /docs, kad pamatytumėte API dokumentaciją!"


@app.get("/products")
def get_all_products() -> list[ItemModel]:
    return products

# New: Get a single product by its ID
@app.get("/products/{item_id}")
def get_product_by_id(item_id: int) -> ItemModel:
    """
    Retrieves a single product by its unique item ID.
    Raises 404 if the item is not found.
    """
    for item in products:
        if item.itemid == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item with itemid {item_id} not found")


@app.post("/products")
def create_new_product(new_product: ItemModel):
    """
    Adds a new product to the system and persists it to the CSV file.
    Raises 400 if a product with the same itemid already exists.
    """
    # Check for duplicate itemid to prevent issues
    for item in products:
        if item.itemid == new_product.itemid:
            raise HTTPException(status_code=400, detail=f"Item with ID {new_product.itemid} already exists.")

    products.append(new_product)
    save_product_to_file(new_product) # Appends to CSV
    return {"message": "New product was successfully added to your shop! :)"}

# New: Update an existing item by its ID
@app.patch("/products/{item_id}") # Using PATCH for partial updates
def update_item(item_id: int, updated_data: ItemUpdateModel):
    """
    Updates the price or quantity_in_stock of an existing product by its item ID.
    Only provided fields in the request body will be updated.
    Raises 404 if the item is not found.
    """
    found_item = None
    # Find the item in the in-memory list
    for item in products:
        if item.itemid == item_id:
            found_item = item
            break

    if found_item is None:
        raise HTTPException(status_code=404, detail=f"Item with itemid {item_id} not found")

    # Apply updates only if the corresponding field is provided in the request body
    if updated_data.price is not None:
        found_item.price = updated_data.price
    if updated_data.quantity_in_stock is not None:
        found_item.quantity_in_stock = updated_data.quantity_in_stock

    # After updating the in-memory list, rewrite the entire CSV file to persist changes
    write_all_products_to_file(products)

    return {"message": f"Item with itemid {item_id} updated successfully", "updated_item": found_item}


@app.get("/number-of-files-in-system")
def number_of_files():
    """
    Returns the number of data rows in the product database CSV file.
    Skips the header row.
    """
    try:
        with open(PATH_TO_DB, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip the header row if there is one
            row_count = sum(1 for _ in reader)
        return {"number_of_files": row_count}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Database file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.delete("/products/{item_id}")
def delete_item(item_id: int):
    """
    Deletes a product from the system by its item ID.
    Persists the change to the CSV file.
    Raises 404 if the item is not found.
    """
    found_index = -1
    for i, item in enumerate(products):
        if item.itemid == item_id:
            found_index = i
            break

    if found_index != -1:
        del products[found_index]
        # After deleting from the in-memory list, rewrite the entire CSV file
        write_all_products_to_file(products)
        return {"message": f"Item with itemid {item_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Item with itemid {item_id} not found")