 # app/domain/service/auth_service.py
from app.platform.jose_utils import decode_jwt
from app.domain.repository.token_repository import store_tokens
from fastapi import HTTPException


async def verify_and_store_token(payload):
    decoded = await decode_jwt(payload.accessToken)
    print("[🔍 JWT 디코딩 결과]", decoded)
    if not decoded or "sub" not in decoded:
        print("[❌ 오류] 디코딩 실패 or sub 없음")
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = decoded["sub"]
    await store_tokens(user_id, payload.accessToken, payload.refreshToken, payload.expiresAt)
    return user_id
