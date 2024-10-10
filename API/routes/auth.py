from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm as FormRequest
from sqlalchemy.orm import Session
from starlette import status
from ..auth import auth_user, create_jwt
from ..data import get_database
from ..models import UserModel
from ..reponse_models import JWTResponse

router = APIRouter(tags=["Auth"], prefix="/auth")

database = Annotated[Session, Depends(get_database)]

@router.post("", status_code=status.HTTP_200_OK, response_model=JWTResponse)
async def get_token(db : database, form_auth : Annotated[FormRequest, Depends()]):
    user_model : UserModel = auth_user(username= form_auth.username, password=form_auth.password, db=db)
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    jwt : str = create_jwt(username=user_model.username, user_id=user_model.user_id)
    return JWTResponse(access_token=jwt)