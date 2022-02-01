from typing import Literal, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    username: str
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    hashed_password: str


class UserUpdateDB(UserBase):
    hashed_password: str
