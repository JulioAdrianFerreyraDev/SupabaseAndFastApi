from pydantic import BaseModel, Field

from .user_request import email_pattern


class EmailRequest(BaseModel):
    email: str = Field(pattern=email_pattern, min_length=5)
