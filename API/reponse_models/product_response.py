from pydantic import BaseModel

from .user_response import UserResponse


class ProductResponse(BaseModel):
    product_id: int
    name: str
    description: str | None
    price: float
    stock: int
    image_url: str
    user: UserResponse
