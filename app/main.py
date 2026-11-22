from itertools import count

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="FastAPI Tutorial")


class ItemInput(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)


class Item(ItemInput):
    id: int


# This tutorial stores items in memory; restarting the server clears them.
items: dict[int, Item] = {}
item_ids = count(1)


def find_item(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.get("/")
def welcome() -> dict[str, str]:
    return {"message": "Welcome to the FastAPI tutorial!"}


@app.get("/hello/{name}")
def hello(name: str, excited: bool = False) -> dict[str, str]:
    punctuation = "!" if excited else "."
    return {"message": f"Hello, {name}{punctuation}"}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(data: ItemInput) -> Item:
    item = Item(id=next(item_ids), **data.model_dump())
    items[item.id] = item
    return item


@app.get("/items")
def list_items() -> list[Item]:
    return list(items.values())


@app.get("/items/{item_id}")
def get_item(item_id: int) -> Item:
    return find_item(item_id)


@app.put("/items/{item_id}")
def update_item(item_id: int, data: ItemInput) -> Item:
    find_item(item_id)
    item = Item(id=item_id, **data.model_dump())
    items[item_id] = item
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> Response:
    find_item(item_id)
    del items[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
