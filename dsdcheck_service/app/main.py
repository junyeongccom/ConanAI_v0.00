import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.dsdcheck_router import router as dsdcheck_router

# 환경변수 로딩
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="DSD Check Service", 
    version="1.0.0",
    description="DSD 공시용 재무데이터 검증 서비스"
)

app.include_router(dsdcheck_router, prefix="/api/dsdcheck") 