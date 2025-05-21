from fastapi import FastAPI
from app.api.esgdsd_router import router as esgdsd_router

app = FastAPI(
    title="ESG DSD Service",
    description="PDF에서 표를 추출해 JSON으로 변환하는 AI 기반 서비스",
    version="0.1.0"
)

# 라우터 등록
app.include_router(esgdsd_router, prefix="/esgdsd", tags=["ESG DSD"])

