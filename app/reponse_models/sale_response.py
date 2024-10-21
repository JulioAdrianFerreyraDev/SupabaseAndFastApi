from datetime import datetime

from pydantic import BaseModel

from .user_response import UserResponse


class SaleResponse(BaseModel):
    sale_id: int
    total_price: float
    sale_date: datetime
    user: UserResponse
