from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.crud.user import crud_user
from app.schemas.user import UserCreate, UserOut, UserInDB, Token
from app.services import user as services
router = APIRouter(prefix="/user")


@router.post("/create", response_model=UserOut)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await services.create_user(user, session)



@router.post("/auth", response_model=Token)
async def auth_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
     return await services.auth_user(user, session)



