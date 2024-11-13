from fastapi import FastAPI, Path, Query, HTTPException, Body, Cookie
from pydantic import BaseModel, Field
from typing import Annotated
from decimal import Decimal
from datetime import datetime, time, timedelta
from uuid import UUID
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

class Item_F(BaseModel):
    name: str
    description: str| None = Field()
    price: float = Field()
    tax: float| None = Field()

@app.post("/items/filter/")
async def filter_item(
                      price_min: Annotated[Decimal, Query()] = None, 
                      price_max: Annotated[Decimal, Query()] = None,
                      tax_included: Annotated[bool, Query()] = None,
                      tags: Annotated[list[str], Query()] = None,
                      ):
    
    return {
        "price_range":[price_min, price_max],
        "tax_included": tax_included,
        "tags": tags,
        "message":"items that match the given filter criteria"
    }

@app.post("/items/create_with_fields/")
async def add_item(
                      item: Annotated[Item_F, Body()], 
                      important: Annotated[int, Body()] = None
                      ):
    
    return {
        "item": item,
        "important": important
    }

@app.post("/items/offers/")
async def add_offer(
                      name: Annotated[str, Body()],
                      discount: Annotated[float, Body()],
                      items: Annotated[list[Item_F], Body()]
                      ):
    
    return {
        "offer": name,
        "items": items,
        "discount": discount
    }

@app.post("/items/users/")
async def add_user(
                      username: Annotated[str, Body()],
                      email: Annotated[str, Body()],
                      full_name: Annotated[str, Body()]
                      ):
    
    return {
        "username": username,
        "email": email,
        "full_name": full_name
    }

@app.post("/items/extra_data_types/")
async def add_extra_data(
                      start_time: Annotated[datetime, Body()],
                      end_time: Annotated[datetime, Body()],
                      repeat_every: Annotated[timedelta, Body()],
                      process_id: Annotated[UUID, Body()]
                      ):
    
    return {
        "start_time": start_time,
        "end_time": end_time,
        "repeat_every": repeat_every,
        "process_id": process_id
    }

@app.post("/items/cookies/")
async def read_item_from_cookie(
                      session_id: Annotated[str, Cookie()]
                      ):
    return{
        "session_id" : session_id,

    }