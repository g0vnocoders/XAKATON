from typing import Any, List, Optional

from pydantic import BaseModel
import time
import types
class ItemBase(BaseModel):
    title: str
    name: str
    description: Optional[str] = None

    start: str# = Column(Time,nullable=False) чч:мм:сс
    end: str#= Column(Time,nullable=False)
    days: int#= Column(Integer,nullable=False) #1111111 days = 127


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
