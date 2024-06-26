from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()


users = [
    {"id": 1, "role": "trader", "name": "Alex"},
    {"id": 2, "role": "trader", "name": "Bob"},
    {"id": 3, "role": "investor", "name": "Sanyok"},
]

fake_trades = [
    {"id": 1, "user_id": 1, "amount": 100},
    {"id": 2, "user_id": 1, "amount": 200},
    {"id": 2, "user_id": 2, "amount": 300},
]


class Trade(BaseModel):
    id: int
    user_id: int
    amount: float = Field(ge=0)


class DegreeType(Enum):
    newbie = "Newbie"
    expert = "Expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]]


@app.get("/")
def hello():
    return {"hello": "world"}


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in users if user.get("id") == user_id]


@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


@app.post("/users/{user_id}")
def change_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, users))[
        0
    ]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}


@app.post("/trades")
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
