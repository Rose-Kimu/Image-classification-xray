from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
@app.get("/")
def first_example():
    return {"GFG Example": "FastAPI"}


#In memory database (for demonstration purposes)
items = []

#Pydantic model for item data
class Item(BaseModel):
    name:str
    description:str

#Create an item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/{item_id}", response_model = Item)
async def read_item(item_id:int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
        return items[item_id]