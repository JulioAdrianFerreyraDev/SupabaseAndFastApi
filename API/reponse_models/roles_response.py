from pydantic import BaseModel, Field


class RolesResponse(BaseModel):
    role_id: int = Field(exclude=True)
    role: str
