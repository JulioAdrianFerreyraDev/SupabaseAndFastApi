from pydantic import BaseModel, Field

from app.reponse_models import ProductResponse, SaleResponse


class SoldProductsResponse(BaseModel):
    id: int
    quantity: int
    product_id: int = Field(exclude=True)
    sale_id: int = Field(exclude=True)
    products: ProductResponse
    sales: SaleResponse
