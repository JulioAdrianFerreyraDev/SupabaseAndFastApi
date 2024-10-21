from fastapi import APIRouter, status, Depends, HTTPException, Path, Query, File, UploadFile

from ..models import ProductModel
from ..reponse_models import ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from ..data import get_database, upload_file, update_file, delete_file
from ..auth import get_current_token
from ..requests_models import ProductRequest, product_form

database = Annotated[Session, Depends(get_database)]
user_dependency = Annotated[dict, Depends(get_current_token)]
product_request_form = Annotated[ProductRequest, Depends(product_form)]
default_image_url: str = "https://dzmpeskjgukecrebnptg.supabase.co/storage/v1/object/public/file_storage/default_images/new-product-presentation.png"


def is_empty(value: str):
    if isinstance(value, str):
        return value == ""


def get_old_file_name(url: str):
    values: list[str] = url.split("/")
    return values[-1]


@router.post(path="", status_code=status.HTTP_204_NO_CONTENT)
async def add_new_product(db: database, user: user_dependency,
                          product_request: product_request_form,
                          image: UploadFile = File()):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    product_model: ProductModel = ProductModel(
        name=product_request.name,
        description=product_request.description,
        price=product_request.price,
        stock=product_request.stock,
        user_id=user_id,
        image_url=await upload_file(file=image)

    )
    db.add(product_model)
    db.commit()


@router.get(path="", status_code=status.HTTP_200_OK, response_model=list[ProductResponse])
async def get_all_products(db: database, user: user_dependency, category: Optional[str] = Query(default=""),
                           name: Optional[str] = Query(default="")):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    products: list[ProductModel] = db.query(ProductModel).filter(ProductModel.user_id == user_id).filter(
        ProductModel.name.like(f"%{name}%")).all()
    return products


@router.get(path="/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def get_product(db: database, user: user_dependency, product_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    product_model: ProductModel | None = db.query(ProductModel).filter(
        ProductModel.product_id == product_id).filter(ProductModel.user_id == user_id).first()
    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product_model


# TODO GET BY CATEGORY

@router.put(path="/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(db: database, user: user_dependency, product_request: product_request_form,
                         image: Optional[UploadFile] | str = File(default=None),
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
    product_model.image_url = product_model.image_url if is_empty(image) else await update_file(
        old_file_name=get_old_file_name(
            product_model.image_url),
        new_file=image)
    db.add(product_model)
    db.commit()


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
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
    delete_file(file_name=get_old_file_name(product_model.image_url))
