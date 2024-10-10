from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from ..auth import get_current_token
from ..data import get_database
from ..models import UserModel

database = Annotated[Session, Depends(get_database)]
user_dependency = Annotated[dict, Depends(get_current_token)]

router = APIRouter(tags=["Admin"], prefix="/admin")


## USERS

@router.get("/users", status_code=status.HTTP_200_OK, description="Admin Only")
async def get_all_users(db: database):
    return db.query(UserModel).filter().all()


## add admin role validation instead of id
@router.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(db: database, user: user_dependency, user_id: int = Path(gt=0)):
    if user is None or user_id != user.get("id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_model: UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_model


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: database, user: user_dependency, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_model: UserModel = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user_model)
    db.commit()
