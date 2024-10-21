from datetime import datetime, timedelta, timezone
from os import getenv
from typing import Annotated

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from ..models import UserModel

load_dotenv()

__SECRET_KEY = getenv("JWT_SECRET_KEY")
__ALGORITHM = "HS256"
__ROLES = {1: "admin", 2: "user", 3: "guest"}


def auth_user(username: str, password: str, db):
    user_model: UserModel = db.query(UserModel).filter(UserModel.username == username).first()
    if user_model is None or not user_model.is_active:
        return None
    if not user_model.validate_password(password):
        return None
    return user_model


def get_role_name(role_id: int) -> str:
    return __ROLES.get(role_id)


def create_jwt(username: str, user_id: int, role: str):
    encode: dict = {"sub": username, "id": user_id, "role": role}
    expiration: datetime = datetime.now(timezone.utc) + timedelta(minutes=30)
    encode.update({"exp": expiration})
    return jwt.encode(encode, __SECRET_KEY, __ALGORITHM)


__auth_token_endpoint = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_token(token: Annotated[str, Depends(__auth_token_endpoint)]):
    try:
        payload: dict = jwt.decode(token, __SECRET_KEY, algorithms=[__ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = int(payload.get("id"))
        expiration_time: datetime = payload.get("exp")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return {"username": username, "id": user_id, "expiration": expiration_time, "role": role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
