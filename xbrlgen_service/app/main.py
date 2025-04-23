from fastapi import FastAPI
from app.api.xbrlgen_router import router as xbrl_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(xbrl_router, prefix="/xbrlgen")

# 허용할 origin 설정 (프론트 주소)
origins = [
    "http://localhost:3000",  # 개발 중일 때
    # "https://your-frontend-domain.com"  # 배포 후 추가
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # 허용할 프론트엔드 도메인
    allow_credentials=True,
    allow_methods=["*"],                # 모든 메소드 허용
    allow_headers=["*"],                # 모든 헤더 허용
)
