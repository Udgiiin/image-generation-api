import base64
import hashlib
import hmac
import secrets
import string
import os
import jwt
from passlib.context import CryptContext
from app.models import User
from app.core.config import settings
from datetime import datetime, timedelta
from typing import Any, Callable, Optional
from functools import wraps
from fastapi import HTTPException
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

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
    actual = hashlib.pbkdf2_hmac(
        settings.ALGORITHM,
        password.encode('utf-8'),
        record.salt.encode('latin-1'),
        int(record.rounds)
    )
    expected = record.hashed_password.encode('latin-1')
    if hmac.compare_digest(actual, expected):
        # create access_token
        access_token = await create_authorisation_token(record.id)

        return {
            "access_token": access_token
        }

    return {}


def decode_jwt_token(token, secret):
    return jwt.decode(token, secret, algorithms=['HS256'])


async def encode_password(password, salt=None):
    if salt is None:
        salt = os.urandom(32)
    rounds = 100000
    hashed = hashlib.pbkdf2_hmac(settings.ALGORITHM, password.encode('utf-8'),
                                 salt, rounds)
    return {
        'salt': salt.decode("latin-1"),
        'rounds': rounds,
        'hashed': hashed.decode("latin-1"),
    }


def auth_required(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        try:
            access_token = kwargs['authorization']
            decoded = decode_jwt_token(access_token, settings.SECRET)
            kwargs['user_id'] = decoded['sub']
            return await func(*args, **kwargs)
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.ExpiredSignatureError) as e:
            raise HTTPException(
                status_code=403,
                detail=f"{e}",
            )


    return wrapper