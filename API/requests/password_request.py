from pydantic import BaseModel, Field

class PasswordRequest(BaseModel):
    password : str = Field(min_length=8, max_length=16)
    new_password : str = Field(min_length=8, max_length=16)
