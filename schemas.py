from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    name: str
    age: int
    gender: str
    email: str
    city: str
    interests: List[str]


class UserBaseOptional(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None


class UserCreate(UserBase):
    pass


class UserUpdate(UserBaseOptional):
    id: int


class User(UserBase):
    id: int
