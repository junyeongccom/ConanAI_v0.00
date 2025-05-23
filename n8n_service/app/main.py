import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.n8n_router import router as n8n_router

# .env 파일 로드
load_dotenv()

# 환경변수에서 PORT 가져오기 (기본값: 8088)
PORT = int(os.getenv("PORT", "8088"))

app = FastAPI(
    title="N8N Service",
    description="N8N Workflow Automation Service",
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
app.include_router(n8n_router)

# 서버 실행을 위한 설정
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )
