# app/api/auth_router.py
from fastapi import APIRouter, Request
from app.domain.model.token_schema import TokenPayload
from app.domain.controller.auth_controller import handle_token

router = APIRouter(prefix="/auth")

@router.post("/token")
async def receive_token(payload: TokenPayload, request: Request):
    return await handle_token(payload)
