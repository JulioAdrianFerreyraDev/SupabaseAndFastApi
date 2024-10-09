from ..data import Base
from sqlalchemy import Column, BIGINT, Float, ForeignKey, DateTime
from datetime import datetime, timezone
class SaleModel(Base):
    __tablename__ = "sales"

    sale_id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    total_price = Column(Float)
    sale_date = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(BIGINT, ForeignKey("users.user_id"))
