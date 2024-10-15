from sqlalchemy import Column, BIGINT, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..data import Base


class SaleProductModel(Base):
    __tablename__ = "sales_products"

    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    quantity = Column(Integer)
    product_id = Column(BIGINT, ForeignKey("products.product_id"))
    sale_id = Column(BIGINT, ForeignKey("sales.sale_id"))
    products = relationship("ProductModel", back_populates="sold_products")
    sales = relationship("SaleModel", back_populates="sold_products")
