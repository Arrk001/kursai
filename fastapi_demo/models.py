from pydantic import BaseModel
from typing import Optional

class ItemModel(BaseModel):
    name: str
    price: float
    weight: float
    quantity_in_stock: int
    itemid: int

    # New Pydantic model for updating an item
class ItemUpdateModel(BaseModel):
    # These fields are optional for partial updates
    price: Optional[float] = None
    quantity_in_stock: Optional[int] = None
    # Note: name and weight are intentionally excluded as per your request