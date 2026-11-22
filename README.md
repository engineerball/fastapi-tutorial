# FastAPI Tutorial

A small FastAPI app that shows how to define routes, use path and query parameters, and validate JSON with Pydantic. It stores items in memory, so restarting the server clears all data. No database is needed.

## Setup

Use Python 3.10 or newer. From the project directory, create and activate a virtual environment and install the dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, use `py -m venv .venv` and `.venv\Scripts\Activate.ps1` instead of the first two commands.

## Run the server

```sh
python -m uvicorn app.main:app --reload
```

Visit [interactive API docs](http://127.0.0.1:8000/docs) to try the routes in your browser.

| Method | Path | What it does |
| --- | --- | --- |
| GET | `/` | Returns a welcome message |
| GET | `/hello/{name}?excited=true` | Greets a name from the path; `excited` is an optional boolean query parameter that defaults to `false` |
| POST | `/items` | Creates an item and returns it with a generated ID (201) |
| GET | `/items` | Lists all items |
| GET | `/items/{item_id}` | Gets one item by its integer ID |
| PUT | `/items/{item_id}` | Replaces an item's name and price without changing its ID |
| DELETE | `/items/{item_id}` | Deletes an item (204, no response body) |

To create an item, send a nonempty `name` and a positive `price`:

```sh
curl -X POST http://127.0.0.1:8000/items \
  -H 'Content-Type: application/json' \
  -d '{"name": "Notebook", "price": 4.50}'
```

Use the returned `id` to get, update, or delete the item. `PUT` takes the same JSON fields as `POST`. Looking up a nonexistent item returns 404, and invalid input returns 422.

## Run the tests

With the virtual environment active, run:

```sh
python -m pytest
```

The tests use FastAPI's `TestClient`, so you don't need to start Uvicorn.
