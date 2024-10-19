from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from ..auth import get_current_token
from ..data import get_database
from ..models import UserModel, ProductModel, SaleModel
from ..reponse_models import UserResponse, ProductResponse, SaleResponse

database = Annotated[Session, Depends(get_database)]
user_dependency = Annotated[dict, Depends(get_current_token)]

router = APIRouter(tags=["Admin"], prefix="/admin")


## USERS

@router.get("/users", status_code=status.HTTP_200_OK, description="Admin Only", response_model=list[UserResponse])
async def get_all_users(db: database, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(UserModel).filter().all()


@router.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(db: database, user: user_dependency, user_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_model: UserModel = db.query(UserModel).get(user_id)
    if user_model is None or not user_model.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_model


## Products
@router.get(path="/products", status_code=status.HTTP_200_OK, response_model=list[ProductResponse])
async def get_all_products(db: database, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    products = db.query(ProductModel).all()
    return products


@router.get(path="/products/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def get_all_products(db: database, user: user_dependency, product_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    products = db.query(ProductModel).get(product_id)
    return products


## Sales
@router.get(path="/sales", status_code=status.HTTP_200_OK, response_model=list[SaleResponse])
async def get_all_sales(db: database, user: user_dependency):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    sales = db.query(SaleModel).all()
    return sales


@router.get(path="/sales/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_sales_by_user(db: database, user: user_dependency, user_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_model: UserModel = db.query(UserModel).get(user_id)
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    sales = [sale.sale_to_json() for sale in user_model.sales]
    return sales


@router.get(path="/sales/{sale_id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
async def get_all_sales(db: database, user: user_dependency, sale_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    sales: SaleModel = db.query(SaleModel).get(sale_id)
    return sales


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: database, user: user_dependency, user_id: int = Path(gt=0)):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_model: UserModel = db.query(UserModel).get(user_id)
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user_model)
    db.commit()


# TODO add sold-products end-points

def get_all_sale_products():
    pass


def get_sale_product(sale_id: int):
    pass


def get_sale_product_by_user(user_id: int):
    pass
