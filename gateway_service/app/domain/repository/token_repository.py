from app.foundation.db import get_db 

async def store_tokens(user_id: str, access_token: str, refresh_token: str, expires_at: int):
    conn = await get_db()
    await conn.execute("""
        INSERT INTO user_tokens (user_id, access_token, refresh_token, expires_at)
        VALUES ($1, $2, $3, to_timestamp($4))
        ON CONFLICT (user_id) DO UPDATE
        SET access_token = $2,
            refresh_token = $3,
            expires_at = to_timestamp($4)
    """, user_id, access_token, refresh_token, expires_at)
