from datetime import datetime

from pydantic import BaseModel, Field

from .roles_response import RolesResponse


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    first_name: str
    last_name: str
    password_hash: str = Field(..., exclude=True)
    created_at: datetime
    updated_at: datetime
    is_active: bool
    role: RolesResponse
