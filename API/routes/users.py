from typing import Annotated

from fastapi import APIRouter, Depends
from ..data import get_database
from sqlalchemy.orm import Session
from starlette import status

from ..models import UserModel

router = APIRouter(prefix="/users", tags=["Users"])

database = Annotated[Session, Depends(get_database)]

@router.post("", status_code=status.HTTP_200_OK)
async def get_users(db: database):
    user_model = UserModel(username="julio_ferreyra", password="jafete210403", email="jaft210403@gmail.com", last_name="Julio", first_name="Ferreyra")
    db.add(user_model)
    db.commit()