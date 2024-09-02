from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ItemOut(Item):
    id: int

app = FastAPI()

item_db = []


@app.get("/items/")
async def read_items() -> list[ItemOut]:
    return item_db

@app.post("/items/")
async def create_item(item: Item):
    new_item = {
        "id": len(item_db) + 1,
        **item.model_dump(),
    }

    item_db.append(new_item)
    print(item_db)
    return new_item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    new_item = {
        "id": item_id,
        **item.model_dump(),
    }

    for i in range(len(item_db)):
        if item_db[i]["id"] == item_id:
            item_db[i] = new_item
            break
    
    return new_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for i in range(len(item_db)):
        if item_db[i]["id"] == item_id:
            item_db.pop(i)
            break
    
    return {"msg": "success"}
