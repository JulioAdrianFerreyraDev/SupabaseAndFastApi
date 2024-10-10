from typing import Annotated
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Path
from ..data import get_database
from sqlalchemy.orm import Session
from starlette import status

from ..models import UserModel
from ..requests import UserRequest, PasswordRequest

router = APIRouter(prefix="/users", tags=["Users"])

database = Annotated[Session, Depends(get_database)]

@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def new_user(db: database, user_request : UserRequest):
    user_model : UserModel = UserModel(
        username= user_request.username,
        password= user_request.password,
        email= user_request.email,
        last_name= user_request.last_name,
        first_name= user_request.first_name
        )
    db.add(user_model)
    db.commit()

@router.get("", status_code=status.HTTP_200_OK, description="Admin Only")
async def get_all_users(db : database):
    return db.query(UserModel).all()

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(db : database, user_id : int = Path(gt=0)):
    user_model : UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_model

@router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(db:database, user_request : UserRequest,user_id : int = Path(gt=0)):
    user_model : UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_model.updated_at = datetime.now(timezone.utc)
    user_model.first_name = user_request.first_name,
    user_model.last_name = user_request.last_name,
    user_model.email = user_request.email,
    user_model.username = user_request.username
    db.add(user_model)
    db.commit()

@router.put("/password/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(db:database, password_request : PasswordRequest ,user_id : int = Path(gt=0)):
    user_model : UserModel | None = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user_model.validate_password(password_request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cannot validate Password")
    user_model.password = password_request.new_password
    db.add(user_model)
    db.commit()


@router.put("/suspend/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def suspend_user(db : database, user_id: int = Path(gt=0)):
    user_model : UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_model.is_active = False
    db.add(user_model)
    db.commit()

