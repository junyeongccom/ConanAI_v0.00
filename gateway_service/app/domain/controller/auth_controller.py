# app/domain/controller/auth_controller.py
from app.domain.model.token_schema import TokenPayload
from app.domain.service.auth_service import verify_and_store_token

async def handle_token(payload: TokenPayload):
    result = await verify_and_store_token(payload)
    return {"message": "Token processed", "user": result}
