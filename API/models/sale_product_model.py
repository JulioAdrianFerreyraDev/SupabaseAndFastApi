from ..data import Base
from sqlalchemy import Column, BIGINT,Integer, ForeignKey

class SaleProductModel(Base):
    __tablename__ = "sales_products"

    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    quantity = Column(Integer)
    product_id = Column(BIGINT, ForeignKey("products.product_id"))
    sale_id = Column(BIGINT, ForeignKey("sales.sale_id"))