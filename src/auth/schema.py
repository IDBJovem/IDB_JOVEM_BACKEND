from typing import Optional

from pydantic import BaseModel

class LoginUrlResponse(BaseModel):
    url: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
