# gateway.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, UploadFile, File, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from typing import List, Optional
from app.domain.model.service_type import ServiceType, SERVICE_URLS

# ✅ .env 파일 로드
load_dotenv()

# ✅ FastAPI 앱 및 라우터 생성
app = FastAPI()
gateway_router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 공통 요청 전송 함수
async def forward_request(service: ServiceType, method: str, url_path: str, files=None, params=None, data=None):
    base_url = SERVICE_URLS[service]
    if not base_url:
        raise HTTPException(status_code=500, detail=f"Base URL for service {service} not configured.")
    url = f"{base_url}/{url_path}"
    headers = {'accept': 'application/json'}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                files=files,
                data=data
            )
            return JSONResponse(content=response.json(), status_code=response.status_code)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ✅ dsdgen_service - POST (엑셀 업로드 + 시트 이름)
@gateway_router.post("/dsdgen/upload")
async def upload_dsdgen(
    file: UploadFile = File(...),
    sheet_names: Optional[List[str]] = Query(None, alias="sheet_name")
):
    files = {'file': (file.filename, await file.read(), file.content_type)}
    params = {'sheet_name': sheet_names} if sheet_names else None
    return await forward_request(ServiceType.DSDGEN, "POST", "api/dsdgen/upload", files=files, params=params)

# ✅ xbrlgen_service - GET (엑셀 업로드 조회)
@gateway_router.get("/xbrlgen/upload")
async def get_xbrlgen_upload(
    file: UploadFile = File(...)
):
    files = {'file': (file.filename, await file.read(), file.content_type)}
    return await forward_request(ServiceType.XBRLGEN, "GET", "api/xbrlgen/upload", files=files)

# ✅ xbrlgen_service - POST (xml 다운로드)
@gateway_router.post("/xbrlgen/download")
async def post_xbrlgen_download(
    filename: str
):
    data = {'filename': filename}
    return await forward_request(ServiceType.XBRLGEN, "POST", "api/xbrlgen/download", data=data)

# ✅ 라우터 앱에 등록
app.include_router(gateway_router)

# ✅ 서버 실행
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SERVICE_PORT", 8080))
    uvicorn.run("gateway:app", host="0.0.0.0", port=port, reload=True)
