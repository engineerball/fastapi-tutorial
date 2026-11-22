from itertools import count

import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture
def client(monkeypatch):
    # Give each test its own empty in-memory store and ID sequence.
    monkeypatch.setattr(main, "items", {})
    monkeypatch.setattr(main, "item_ids", count(1))
    with TestClient(main.app) as test_client:
        yield test_client


def test_welcome(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI tutorial!"}


@pytest.mark.parametrize(
    ("query", "message"),
    [("", "Hello, Ada."), ("?excited=true", "Hello, Ada!")],
)
def test_hello(client, query, message):
    response = client.get(f"/hello/Ada{query}")

    assert response.status_code == 200
    assert response.json() == {"message": message}


def test_hello_rejects_invalid_query(client):
    assert client.get("/hello/Ada?excited=maybe").status_code == 422


def test_item_lifecycle(client):
    empty = client.get("/items")
    assert empty.status_code == 200
    assert empty.json() == []

    data = {"name": "Notebook", "price": 4.50}
    created = client.post("/items", json=data)
    assert created.status_code == 201
    item = created.json()
    assert item == {"id": 1, **data}
    path = f"/items/{item['id']}"

    listed = client.get("/items")
    assert listed.status_code == 200
    assert listed.json() == [item]

    fetched = client.get(path)
    assert fetched.status_code == 200
    assert fetched.json() == item

    replacement = {"name": "Sketchbook", "price": 7.25}
    updated = client.put(path, json=replacement)
    assert updated.status_code == 200
    assert updated.json() == {"id": item["id"], **replacement}
    assert client.get(path).json() == updated.json()

    deleted = client.delete(path)
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(path).status_code == 404
    assert client.get("/items").json() == []


@pytest.mark.parametrize("method", ["GET", "PUT", "DELETE"])
def test_missing_item(client, method):
    kwargs = {"json": {"name": "Notebook", "price": 4.50}} if method == "PUT" else {}
    response = client.request(method, "/items/999", **kwargs)

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


@pytest.mark.parametrize(
    "data",
    [{"name": "Notebook"}, {"name": "", "price": 4.50}, {"name": "Notebook", "price": 0}],
)
def test_create_rejects_invalid_item(client, data):
    assert client.post("/items", json=data).status_code == 422
    assert client.get("/items").json() == []
