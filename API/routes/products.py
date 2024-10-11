from fastapi import APIRouter, status, Depends, HTTPException, Path, Query
from starlette.status import HTTP_204_NO_CONTENT

from ..models import ProductModel

router = APIRouter(prefix="/products", tags=["Products"])
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from ..data import get_database
from ..auth import get_current_token
from ..requests_models import ProductRequest

database = Annotated[Session, Depends(get_database)]
user_dependency = Annotated[dict, Depends(get_current_token)]


@router.post(path="", status_code=status.HTTP_204_NO_CONTENT)
async def add_new_product(db: database, user: user_dependency, product_request: ProductRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    product_model: ProductModel = ProductModel(
        name=product_request.name,
        description=product_request.description,
        price=product_request.price,
        stock=product_request.stock,
        image_url=product_request.image_url,
        user_id=user_id
    )
    db.add(product_model)
    db.commit()


@router.get(path="", status_code=status.HTTP_200_OK)
async def get_all_products(db: database, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    products: list[ProductModel] = db.query(ProductModel).filter(ProductModel.user_id == user_id).all()
    return products


@router.get(path="/{product_id}", status_code=status.HTTP_200_OK)
async def get_product(db: database, user: user_dependency, product_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    product_model: ProductModel | None = db.query(ProductModel).filter(
        ProductModel.product_id == product_id).filter(ProductModel.user_id == user_id).first()
    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product_model


# TODO: ADD CATEGORY
@router.get(path="/", status_code=status.HTTP_200_OK)
async def get_products_by_category(db: database, user: user_dependency, category: Optional[str] = Query(default=None)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    return db.query(ProductModel).filter(ProductModel.user_id == user_id).all()


@router.put(path="/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_product(db: database, user: user_dependency, product_request: ProductRequest,
                         product_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    product_model: ProductModel | None = db.query(ProductModel).filter(
        ProductModel.product_id == product_id).filter(ProductModel.user_id == user_id).first()
    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product_model.name = product_request.name
    product_model.stock = product_request.stock
    product_model.price = product_request.price
    product_model.description = product_request.description
    product_model.image_url = product_request.image_url
    db.add(product_model)
    db.commit()


@router.delete("/{product_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(db: database, user: user_dependency, product_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    product_model: ProductModel | None = db.query(ProductModel).filter(ProductModel.product_id == product_id).filter(
        ProductModel.user_id == user_id).first()
    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product_model)
    db.commit()
