from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from ..auth import get_current_token
from ..data import get_database
from ..models import UserModel
from ..reponse_models import UserResponse
from ..requests_models import UserRequest, PasswordRequest

router = APIRouter(prefix="/users", tags=["Users"])

database = Annotated[Session, Depends(get_database)]
user_dependency = Annotated[dict, Depends(get_current_token)]


## READ
@router.get("", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_all_users(db: database):
    return db.query(UserModel).filter(UserModel.is_active == True).filter(UserModel.role_id == 2).all()


@router.get("/current", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_current_user(db: database, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    user_model: UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_model


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(db: database, user: user_dependency, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_model: UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).filter(
        UserModel.is_active == True).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_model


## UPDATE
@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(db: database, user: user_dependency, user_request: UserRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    user_model: UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_model.updated_at = datetime.now(timezone.utc)
    user_model.first_name = user_request.first_name,
    user_model.last_name = user_request.last_name,
    user_model.email = user_request.email,
    user_model.username = user_request.username
    db.add(user_model)
    db.commit()


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(db: database, user: user_dependency, password_request: PasswordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    user_model: UserModel | None = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user_model.validate_password(password_request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot validate Password")
    user_model.password = password_request.new_password
    user_model.updated_at = datetime.now(timezone.utc)
    db.add(user_model)
    db.commit()


@router.put("/suspend", status_code=status.HTTP_204_NO_CONTENT)
async def suspend_user(db: database, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    user_model: UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_model.is_active = False
    db.add(user_model)
    db.commit()
