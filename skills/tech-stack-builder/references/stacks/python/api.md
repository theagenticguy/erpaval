# Python API Stack

Web framework selection for Python APIs. This is a RESEARCH category — choice depends on project type.

## Decision Framework

| Use Case                           | Recommendation | Why                                            |
| ---------------------------------- | -------------- | ---------------------------------------------- |
| Fast API, async, microservice      | **FastAPI**    | Largest ecosystem, best OpenAPI integration    |
| Performance-critical, full control | **Litestar**   | Faster than FastAPI, more opinionated defaults |
| Full-stack web app, admin          | **Django**     | Batteries-included, ORM, admin, auth           |
| Minimal, learning, prototyping     | **Flask**      | Simplest, most docs/tutorials                  |

## FastAPI Quick Start

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}")
async def get_item(item_id: int) -> Item:
    return Item(name="Widget", price=9.99)

@app.post("/items")
async def create_item(item: Item) -> Item:
    return item
```

## Litestar Quick Start

```python
from litestar import Litestar, get, post
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@get("/items/{item_id:int}")
async def get_item(item_id: int) -> Item:
    return Item(name="Widget", price=9.99)

@post("/items")
async def create_item(data: Item) -> Item:
    return data

app = Litestar([get_item, create_item])
```

## Common Patterns

- **Validation**: Pydantic v2 models for request/response (both frameworks use it natively)
- **Database**: SQLAlchemy 2.0 async or SQLModel for ORM (RESEARCH category)
- **Auth**: Depends on model — OAuth2/JWT, session-based, API key
- **CORS**: Built-in middleware in both FastAPI and Litestar
- **Testing**: httpx.AsyncClient + pytest-asyncio
