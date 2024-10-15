from datetime import datetime, timezone

from sqlalchemy import Column, BIGINT, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from ..data import Base


class SaleModel(Base):
    __tablename__ = "sales"

    sale_id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    total_price = Column(Float)
    sale_date = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(BIGINT, ForeignKey("users.user_id"))
    user = relationship("UserModel", back_populates="sales")
    sold_products = relationship("SaleProductModel", back_populates="sales", cascade="all, delete-orphan")
