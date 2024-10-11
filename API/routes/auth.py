from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm as FormRequest
from sqlalchemy.orm import Session
from starlette import status

from ..auth import auth_user, create_jwt
from ..data import get_database
from ..models import UserModel
from ..reponse_models import JWTResponse
from ..requests_models import UserRequest

router = APIRouter(tags=["Auth"], prefix="/auth")

database = Annotated[Session, Depends(get_database)]


## CREATE
@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
async def register(db: database, user_request: UserRequest):
    user_model: UserModel = UserModel(
        username=user_request.username,
        password=user_request.password,
        email=user_request.email,
        last_name=user_request.last_name,
        first_name=user_request.first_name
    )
    db.add(user_model)
    db.commit()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=JWTResponse)
async def login(db: database, form_auth: Annotated[FormRequest, Depends()]):
    user_model: UserModel = auth_user(username=form_auth.username, password=form_auth.password, db=db)
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    jwt: str = create_jwt(username=user_model.username, user_id=user_model.user_id)
    return JWTResponse(access_token=jwt)
