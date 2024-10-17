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

    def sale_to_json(self) -> dict:
        """

        :return:
        """
        return {
            "sale": {
                "sale_id": self.sale_id,
                "sale_date": self.sale_date,
                "total": self.total_price,
                "user": f"{self.user.first_name} {self.user.last_name}",
                "products": [
                    {
                        "product_id": sp.products.product_id,
                        "product_name": sp.products.name,
                        "quantity": sp.quantity,
                        "price": sp.products.price
                    }
                    for sp in self.sold_products
                ]
            }
        }
