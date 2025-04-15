# app/foundation/db.py
import asyncpg
from app.foundation.settings import DATABASE_URL

_db_pool = None

async def connect_db():
    global _db_pool
    _db_pool = await asyncpg.create_pool(
        dsn=DATABASE_URL,     # ✅ 수정: settings에서 가져온 값 사용
        min_size=1,
        max_size=5
    )

async def get_db():
    if _db_pool is None:
        raise Exception("Database not connected. Did you call connect_db()?")

    return _db_pool
