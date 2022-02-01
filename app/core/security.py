import bcrypt
import jwt
from passlib.context import CryptContext
from app.models import User
from app.core.config import settings
from datetime import datetime, timedelta
from typing import Any, Callable
from functools import wraps
from fastapi import HTTPException


def create_token(database_id, secret, exp):
    now = datetime.utcnow()
    exp = datetime.utcnow() + exp
    payload = {
        'sub': database_id,
        'iat': now,
        'nbf': now,
        "exp": exp,
    }
    return jwt.encode(payload, secret, algorithm='HS256')



async def create_authorisation_token(username):
    access_token = create_token(username, settings.SECRET,
                                timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),

    return list(access_token).pop()


async def get_jwt_token(record: User, password ):
    if bcrypt.checkpw(password.encode('utf-8'), record.hashed_password.encode('utf-8')):
        access_token = await create_authorisation_token(record.id)
        return {
            "access_token": access_token
        }

    raise HTTPException(
        status_code=406,
        detail="wrong password"
    )


def decode_jwt_token(token):
    return jwt.decode(token, settings.SECRET, algorithms=['HS256'])


async def encode_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return {
        'hashed': hashed.decode('utf-8'),
    }


def auth_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        try:
            access_token = kwargs['authorization']
            decoded = decode_jwt_token(access_token)
            kwargs['user_id'] = decoded['sub']
            return await func(*args, **kwargs)
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignatureError, jwt.exceptions.DecodeError) as e:
            raise HTTPException(
                status_code=403,
                detail=f"{e}",
            )


    return wrapper