from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Path
from fastapi.params import Depends
from sqlalchemy.orm import Session

from ..auth import get_current_token
from ..data import get_database
from ..models import SaleModel
from ..reponse_models import SaleResponse
from ..requests_models import SaleRequest

router = APIRouter(prefix="/sales", tags=["Sales"])

database = Annotated[Session, Depends(get_database)]
user_dependency = Annotated[dict, Depends(get_current_token)]


# CREATE
@router.post("", status_code=status.HTTP_204_NO_CONTENT)
async def add_new_sale(db: database, user: user_dependency, sale_request: SaleRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    sale_model: SaleModel = SaleModel(
        user_id=user_id,
        total_price=sale_request.total_price,
        sale_date=sale_request.sale_date
    )
    db.add(sale_model)
    db.commit()


# READ
@router.get("", status_code=status.HTTP_200_OK, response_model=list[SaleResponse])
async def get_all_sales(db: database, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    return db.query(SaleModel).filter(SaleModel.user_id == user_id).all()


@router.get("/{sale_id}", status_code=status.HTTP_200_OK, response_model=SaleResponse)
async def get_sale(db: database, user: user_dependency, sale_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    sale_model: SaleModel | None = db.query(SaleModel).filter(SaleModel.sale_id == sale_id).filter(
        SaleModel.user_id == user_id).first()
    if sale_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sale found")
    return sale_model


# UPDATE
@router.put("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_sale(db: database, user: user_dependency, sale_request: SaleRequest, sale_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    sale_model: SaleModel | None = db.query(SaleModel).filter(SaleModel.sale_id == sale_id).filter(
        SaleModel.user_id == user_id).first()
    if sale_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sale found")
    sale_model.total_price = sale_request.total_price
    db.add(sale_model)
    db.commit()


# DELETE
@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale(db: database, user: user_dependency, sale_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    user_id: int = user.get("id")
    sale_model: SaleModel | None = db.query(SaleModel).filter(SaleModel.sale_id == sale_id).filter(
        SaleModel.user_id == user_id).first()
    if sale_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sale found")
    db.delete(sale_model)
    db.commit()
