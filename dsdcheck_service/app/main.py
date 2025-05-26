from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.dsdfooting_router import router as dsdfooting_router

app = FastAPI(
    title="재무제표 검증 서비스",
    description="재무제표 엑셀 파일의 합계검증을 수행하는 API 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(dsdfooting_router)

@app.get("/")
async def root():
    return {"message": "재무제표 검증 서비스 API"} 