from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    price: str
    volume: str
    funds: str
    market: str
    created_at: str

class ItemList(BaseModel):
    item_list: List[Item] = []
