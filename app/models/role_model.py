from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from ..data import Base


class RolesModel(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)
    user = relationship("UserModel", back_populates="role", cascade="all, delete-orphan")
