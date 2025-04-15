# app/domain/model/token_schema.py
from pydantic import BaseModel

class TokenPayload(BaseModel):
    accessToken: str
    refreshToken: str
    expiresAt: int
