from sqlalchemy import Column, BIGINT, String, Text, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..data import Base


class ProductModel(Base):
    __tablename__ = "products"

    product_id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    image_url = Column(Text,
                       default="https://imgs.search.brave.com/lRV2F48bPPe-Dl_4JARbjs-dXDKxn-ZB2eqBpYYMhFU/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTg0/Mzc3NDc1L3Bob3Rv/L25ldy1wcm9kdWN0/LXByZXNlbnRhdGlv/bi5qcGc_cz02MTJ4/NjEyJnc9MCZrPTIw/JmM9blRlNDk2aHRm/T0dwcF91NnJ3RzBZ/b3FnMWNicC1ZWjVB/TkJSZFNuOUUtQT0")
    user_id = Column(BIGINT, ForeignKey("users.user_id"))
    user = relationship("UserModel", back_populates="products")
