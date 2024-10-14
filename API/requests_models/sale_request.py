from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class SaleRequest(BaseModel):
    total_price: float = Field(gt=0)
    sale_date: Optional[datetime] = Field(default=datetime.now(timezone.utc), exclude=True)
