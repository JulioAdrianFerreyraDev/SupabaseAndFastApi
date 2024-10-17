from datetime import datetime, timezone

from passlib.context import CryptContext
from sqlalchemy import Column, String, Boolean, BIGINT, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from ..data import Base

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
roles = {"admin": 1, "user": 2, "guest": 3}


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(BIGINT, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    sales = relationship("SaleModel", back_populates="user", cascade="all, delete-orphan")
    products = relationship("ProductModel", back_populates="user", cascade="all, delete-orphan")
    role = relationship("RolesModel", back_populates="user")

    @property
    def password(self):
        raise ValueError("Cannot access to this value")

    @password.setter
    def password(self, plain_password: str):
        self.password_hash = bcrypt_context.hash(plain_password)

    @property
    def role_name(self):
        match self.role_id:
            case 1:
                return "admin"
            case 2:
                return "user"
            case 3:
                return "guest"

    @role_name.setter
    def role_name(self, role: str):
        self.role_id = roles.get(role)

    def validate_password(self, plain_password: str) -> bool:
        return bcrypt_context.verify(plain_password, self.password_hash)

    def __init__(self, username,
                 email,
                 first_name,
                 last_name,
                 password,
                 role: str
                 ):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_active = True
        self.role_name = role
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
