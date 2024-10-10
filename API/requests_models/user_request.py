from typing import Optional

from pydantic import BaseModel, Field

email_pattern : str = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
class UserRequest(BaseModel):
    user_id : Optional[int] = Field(gt=0, default=None, description="Required only when updating")
    username : str = Field(min_length=3, max_length=16, examples=["username"])
    email : str = Field(min_length=5, pattern=email_pattern, examples=["example@mail.com"])
    first_name : str = Field(min_length=3)
    last_name : str = Field(min_length=3)
    password : str = Field(min_length=8, max_length=10, examples=["password"])
