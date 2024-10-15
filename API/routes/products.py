from fastapi import APIRouter, status, Depends, HTTPException, Path, Query, File, UploadFile, Form

from ..models import ProductModel
from ..reponse_models import ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from ..data import get_database, upload_file
from ..auth import get_current_token
from ..requests_models import ProductRequest

database = Annotated[Session, Depends(get_database)]
user_dependency = Annotated[dict, Depends(get_current_token)]


def get_product_info(description: Optional[str] = Form(default=""), price: float = Form(), stock: int = Form(),
                     name: str = Form()):
    return ProductRequest(product_id=None, description=description, price=price, stock=stock, name=name)


@router.post(path="", status_code=status.HTTP_204_NO_CONTENT)
async def add_new_product(db: database, user: user_dependency,
                          product_request: ProductRequest = Depends(get_product_info),
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
        image_url=await upload_file(username=user.get("username"), file=image)

    )
    db.add(product_model)
    db.commit()


@router.get(path="", status_code=status.HTTP_200_OK, response_model=list[ProductResponse])
async def get_all_products(db: database, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    products: list[ProductModel] = db.query(ProductModel).filter(ProductModel.user_id == user_id).all()
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


# TODO: ADD CATEGORY
@router.get(path="/", status_code=status.HTTP_200_OK)
async def get_products_by_category(db: database, user: user_dependency, category: Optional[str] = Query(default=None)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    return db.query(ProductModel).filter(ProductModel.user_id == user_id).all()


@router.put(path="/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_product(db: database, user: user_dependency, product_request: ProductRequest,
                         image: UploadFile = File(),
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
    product_model.image_url = "https://uppkqkteqxmhxkbuvani.supabase.co/storage/v1/object/sign/file_storage/new-product-presentation.png?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJmaWxlX3N0b3JhZ2UvbmV3LXByb2R1Y3QtcHJlc2VudGF0aW9uLnBuZyIsImlhdCI6MTcyOTAxMzQ4OSwiZXhwIjoxNzYwNTQ5NDg5fQ.vu1TuZUWJgUg2MzGBwiM3bc2y2-aBmeS9y5ZkUjPH_4&t=2024-10-15T17%3A31%3A31.463Z"
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
