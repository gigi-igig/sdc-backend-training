from fastapi import FastAPI, Query, Body, Cookie, Path, HTTPException
from typing import Annotated
from decimal import Decimal
from pydantic import BaseModel, Field
from datetime import datetime, time, timedelta
from uuid import UUID
app = FastAPI()

class Item(BaseModel):
    item_id: int = None
    name: str = "Test Item"
    description: str = "A test description"
    price: Decimal = 10.5
    tax: Decimal = 1.5

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(
        item_id: Annotated[Decimal, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000.")], 
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
                      item_id: Annotated[Decimal, Path(ge=1, le=1000, description="Item ID must be between 1 and 1000.")], 
                      item: Item = None, 
                      q: Annotated[str | None, Query(min_length=3, max_length=50, description="Query 'q' must be between 3 and 50 characters.")] = None
                      ):
    updated_item = item.model_dump()
    response = {"item_id": item_id, **updated_item}

    if q:
        response.update({"q": q})
    
    return response

class Item_1(BaseModel):
    name: str
    description: str| None = Field(default=None, title="The description of the item")
    price: float = Field(gt = 0., description="The price of the item must greater than zero")
    tax: float = Field(gt = 0., description="The tax of the item must greater than zero")

@app.post("/items/filter/")
async def read_items(
    price_min: Annotated[int , Query(description = "Minimum price of the item")] = None,
    price_max: Annotated[int , Query(description = "Maximum price of the item")] = None,
    tax_included: Annotated[bool, Query(description = "Boolean indicating whether tax is included in the price")] = None,
    tags: Annotated[list[str], Query(description="List of tags to filter items")] = None
    ):
    return {
        "price_range": [price_min, price_max],
        "tax_included": tax_included,
        "tags": tags,
        "message": "This is a filtered list of items based on the provided criteria."
    }
@app.post("/items/create_with_fields/")
async def add_item(
    item: Annotated[Item_1, Body()],
    importance: Annotated[int , Body()]
):
    return {
        "item": item,
        "importance": importance
    }
@app.post("/offers/")
async def add_offer(
    name: Annotated[str, Body()],
    discount: Annotated[float, Body()],
    items: Annotated[list[Item_1], Body()]
):
    return {
        "offer_name": name,
        "discount": discount,
        "items": items
    }
@app.post("/users/")
async def add_user(
    username: Annotated[str, Body()],
    email: Annotated[str, Body()],
    full_name: Annotated[str, Body()],
):
    return {
        "username": username,
        "email": email,
        "full_name": full_name
    }
@app.post("/items/extra_data_types/")
async def add_extra_data_types(
    start_time: Annotated[datetime, Body()],
    end_time: Annotated[time, Body()],
    repeat_every: Annotated[timedelta, Body()],
    process_id: Annotated[UUID, Body()]
):
    return {
        "message": "This is an item with extra data types.",
        "start_time": start_time,
        "end_time": end_time,
        "repeat_every": repeat_every,
        "process_id": process_id
        
    }
@app.get("/items/cookies/")
async def read_items_from_cookies(
    session_id: Annotated[str, Cookie(description="Session ID for authentication")]
):
    return {
        "session_id": session_id,
        "message": "This is the session ID obtained from the cookies."
    }