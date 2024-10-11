from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from ..models import UserModel

__SECRET_KEY = "a100cbe71ba07c4718179eff6cdcd6e84f3ca4c7959c771cd95012f411e1efe6"
__ALGORITHM = "HS256"


def auth_user(username: str, password: str, db):
    user_model: UserModel = db.query(UserModel).filter(UserModel.username == username).first()
    if user_model is None or not user_model.is_active:
        return None
    if not user_model.validate_password(password):
        return None
    return user_model


def create_jwt(username: str, user_id: int):
    encode: dict = {"sub": username, "id": user_id}
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
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        return {"username": username, "id": user_id, "expiration": expiration_time}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
