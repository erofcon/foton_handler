from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    username: str
    is_super_user: bool


class TokenData(BaseModel):
    username: str | None = None
