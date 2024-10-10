from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel
from typing import Annotated
from decimal import Decimal
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str| None = None
    price: float
    tax: float| None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(
        item_id: Annotated[Decimal, Path(gt=1, lt=1000, description="Item ID must be between 1 and 1000.")], 
        q: Annotated[str | None, Query(min_length=3, max_length=50, description="Query 'q' must be between 3 and 50 characters.")] = None, 
        sort_order: str = "asc"
    ):

    response = {
        "item_id": item_id,
        "description": f"This is a sample item that matches the query {q}" if q else "This is a sample item.",
        "sort_order": sort_order
    }
    
    return response


@app.put("/items/{item_id}")
async def update_item(
                      item_id: Annotated[Decimal, Path(gt=1, lt=1000, description="Item ID must be between 1 and 1000.")], 
                      item: Item, 
                      q: Annotated[str | None, Query(min_length=3, max_length=50, description="Query 'q' must be between 3 and 50 characters.")] = None
                      ):
    updated_item = item.model_dump()
    response = {"item_id": item_id, **updated_item}

    if q:
        response["q"] = q
    
    return response