from typing import Optional

from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    product_id: Optional[int] = Field(gt=0, default=None)
    name: str = Field(min_length=3)
    description: Optional[str] = Field(default="")
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
