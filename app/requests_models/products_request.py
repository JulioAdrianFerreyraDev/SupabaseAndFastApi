from typing import Optional

from fastapi import Form
from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    product_id: Optional[int] = Field(gt=0, default=None)
    name: str = Field(min_length=3)
    description: Optional[str] = Field(default="")
    price: float = Field(ge=0)
    stock: int = Field(ge=0)


def get_product_info(description: Optional[str] = Form(default=""), price: float = Form(), stock: int = Form(),
                     name: str = Form()):
    return ProductRequest(product_id=None, description=description, price=price, stock=stock, name=name)
