from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for request body
class Item(BaseModel):
    name: str
    price: float
    available: bool = True

# Fake database (dictionary)
fake_db = {}


# -------------------------------
# GET (all items)
@app.get("/items/")
def get_items():
    return {"items": fake_db}


# GET (single item by ID)
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id in fake_db:
        return {"item_id": item_id, "item": fake_db[item_id]}
    return {"error": "Item not found"}


# POST (create new item)
@app.post("/items/")
def create_item(item: Item):
    item_id = len(fake_db) + 1
    fake_db[item_id] = item.dict()
    return {"message": "Item created", "item_id": item_id, "item": item}


# PUT (replace an existing item)
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id in fake_db:
        fake_db[item_id] = item.dict()
        return {"message": "Item replaced", "item_id": item_id, "item": item}
    return {"error": "Item not found"}


# PATCH (partially update an item)
@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    if item_id in fake_db:
        # Update only provided fields
        stored_item = fake_db[item_id]
        stored_item.update(item.dict(exclude_unset=True))
        fake_db[item_id] = stored_item
        return {"message": "Item partially updated", "item_id": item_id, "item": fake_db[item_id]}
    return {"error": "Item not found"}


# DELETE (remove an item)
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in fake_db:
        deleted_item = fake_db.pop(item_id)
        return {"message": "Item deleted", "deleted_item": deleted_item}
    return {"error": "Item not found"}
