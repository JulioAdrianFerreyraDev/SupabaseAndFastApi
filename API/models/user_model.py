from ..data import Base
from sqlalchemy import Column, String, Boolean, BIGINT, DateTime
from datetime import datetime, timezone
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(BIGINT, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    @property
    def password(self):
        raise ValueError("Cannot access to this value")

    @password.setter
    def password(self, plain_password: str):
        self.password_hash = bcrypt_context.hash(plain_password)

    def validate_password(self, plain_password: str) -> bool:
        return bcrypt_context.verify(plain_password, self.password_hash)

    def __init__(self, username,
                 email,
                 first_name,
                 last_name,
                 password):
        self.username = username,
        self.email = email,
        self.first_name = first_name,
        self.last_name = last_name,
        self.password = password
        self.is_active = False
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

