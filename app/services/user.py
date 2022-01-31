from app.core.security import encode_password
from fastapi import Depends, HTTPException
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import crud_user
from app.schemas.user import UserInDB
from app.core.security import get_jwt_token


async def create_user(user, session: AsyncSession):
    security_data = await encode_password(user.password)
    user_db = await crud_user.get(session, username=user.username)
    if user_db is not None:
        raise HTTPException(
            status_code=409,
            detail="The user with this username already exists in the system",
        )
    obj_in = UserInDB(
        **user.dict(), hashed_password=security_data['hashed'], salt=security_data['salt'], rounds=security_data['rounds']
    )
    return await crud_user.create(session, obj_in)


async def auth_user(user, session: AsyncSession):
    user_db = await crud_user.get(session, username=user.username)
    if user_db is None:
        raise HTTPException(
            status_code=409,
            detail="username is exists",
        )
    return await get_jwt_token(user_db, user.password)
