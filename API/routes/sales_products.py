from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Path
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ..auth import get_current_token
from ..data import get_database
from ..models import SaleProductModel, SaleModel, UserModel, ProductModel
from ..reponse_models import SoldProductsResponse
from ..requests_models.sold_products_request import SoldProductsRequest

router = APIRouter(prefix="/sold/products", tags=["Sold Products"])

database = Annotated[Session, Depends(get_database)]
user_dependency = Annotated[dict, Depends(get_current_token)]


# CREATE
@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def add_sold_products(db: database, user: user_dependency, sold_products: list[SoldProductsRequest]):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    for sale in sold_products:
        sale_model: SaleProductModel = SaleProductModel(**sale.model_dump())
        product_model: ProductModel = db.query(ProductModel).get(sale_model.product_id)
        if product_model.stock < sale_model.quantity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Not enough items")
        product_model.stock -= sale_model.quantity
        sale_model.id = None
        db.add(sale_model)
        db.add(product_model)
        db.commit()


# READ
@router.get("", status_code=status.HTTP_200_OK, response_model=list[SoldProductsResponse])
async def get_all(db: database, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return db.query(SaleProductModel).all()


@router.get(path="/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_current_user_sales(db: database, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    user_model: UserModel = db.query(UserModel).get(user_id)
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    sales = [sale.sale_to_json() for sale in user_model.sales]
    return sales


@router.get("/{sale_id}", status_code=status.HTTP_200_OK)
async def get_sold_products_by_sale(db: database, user: user_dependency, sale_id: int = Path(gt=0)):
    """
    :param db:
    :param user:
    :param sale_id:
    :return:
    """
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    sale_model: SaleModel = db.query(SaleModel).filter(SaleModel.user_id == user_id).filter(
        SaleModel.sale_id == sale_id).first()
    if sale_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return sale_model.sale_to_json()


@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update_sale_product(db: database, user: user_dependency, sale: SoldProductsRequest,
                              ):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    sp: SaleProductModel = db.query(SaleProductModel).filter(SaleProductModel.sale_id == sale.sale_id).filter(
        SaleProductModel.product_id == sale.product_id).first()
    if sp is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    product_model: ProductModel = db.query(ProductModel).get(sp.product_id)
    product_model.stock += sp.quantity - sale.quantity
    sp.quantity = sale.quantity
    db.add(sp)
    db.add(product_model)
    db.commit()


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale_product(db: database, user: user_dependency, sale_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    sp: list = db.query(SaleProductModel).filter(SaleProductModel.sale_id == sale_id).all()
    if len(sp) != 0 and sp[0].sales.user.user_id != user.get("id"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not Found")
    for sale in sp:
        db.delete(sale)
    db.commit()
