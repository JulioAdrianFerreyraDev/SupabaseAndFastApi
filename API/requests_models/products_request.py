from typing import Optional

from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    product_id: Optional[int] = Field(gt=0, default=None)
    name: str = Field(min_length=3)
    description: Optional[str] = Field(default="")
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    image_url: Optional[str] = Field(
        default="https://imgs.search.brave.com/lRV2F48bPPe-Dl_4JARbjs-dXDKxn-ZB2eqBpYYMhFU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTg0/Mzc3NDc1L3Bob3Rv/L25ldy1wcm9kdWN0/LXByZXNlbnRhdGlv/bi5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9blRlNDk2aHRm/T0dwcF91NnJ3RzBZ/b3FnMWNicC1ZWjVB/TkJSZFNuOUUtQT0")
