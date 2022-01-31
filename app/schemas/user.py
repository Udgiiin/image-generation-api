from typing import Literal, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str = None


class TokenPayload(BaseModel):
    user_id: Optional[int]


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
    salt: str
    rounds: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserUpdateDB(UserBase):
    hashed_password: str
