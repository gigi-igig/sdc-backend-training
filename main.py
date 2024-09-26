from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from typing import Annotated
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str| None = None
    price: float
    tax: float| None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Annotated[str | None, Query(max_length=50)] = None):
    updated_item = item.model_dump()
    response = {"item_id": item_id, **updated_item}

    if q:
        response["q"] = q
    
    return response