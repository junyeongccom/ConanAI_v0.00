from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.xbrlgen_router import router as xbrl_router

app = FastAPI(
    title="XBRL Generator API",
    description="XBRL 및 DSD 생성을 위한 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 개발 서버
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# 라우터에 이미 prefix가 설정되어 있으므로 추가 prefix 없이 등록
app.include_router(xbrl_router)
