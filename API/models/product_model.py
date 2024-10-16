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
                       default="https://dzmpeskjgukecrebnptg.supabase.co/storage/v1/object/public/file_storage/default_images/new-product-presentation.png")
    user_id = Column(BIGINT, ForeignKey("users.user_id"))
    user = relationship("UserModel", back_populates="products")
    sold_products = relationship("SaleProductModel", back_populates="products", cascade="all, delete-orphan")
