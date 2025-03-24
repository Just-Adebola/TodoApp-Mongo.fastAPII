from datetime import datetime
from pydantic import BaseModel
from typing import Union
from uuid import UUID


class UserBase(BaseModel):
    username: str


class User(BaseModel):
    id: str
    created_at: Union[datetime, str] = datetime.now()


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass