from typing import Optional

from pydantic import Field, BaseModel


class SoldProductsRequest(BaseModel):
    id: Optional[int] = Field(default=None)
    quantity: int = Field(gt=0)
    product_id: int = Field(gt=0)
    sale_id: int = Field(gt=0)
