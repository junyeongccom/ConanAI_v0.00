from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.auth_router import router as auth_router
from app.foundation.db import connect_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield

# ✅ FastAPI 인스턴스는 단 한 번 선언
app = FastAPI(title="API Gateway", lifespan=lifespan)

# ✅ API 라우터 정의 및 라우터 등록
api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
app.include_router(api_router)

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_router.get("/")
async def root():
    return {"message": "Welcome to API Gateway"}
