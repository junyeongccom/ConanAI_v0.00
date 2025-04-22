from fastapi import APIRouter, UploadFile, File, Body
from app.domain.controller.xbrlgen_controller import XBRLGenController
import os
from fastapi.responses import FileResponse, HTMLResponse, Response
import aiofiles
from typing import Dict, Any, List
from pydantic import BaseModel

class GenerateRequest(BaseModel):
    filename: str
    data: List[Dict[str, Any]]

# 라우터에 prefix 추가
router = APIRouter(
    prefix="/xbrlgen",
    tags=["XBRL Generator"],
    responses={404: {"description": "Not found"}}
)
controller = XBRLGenController()

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    """
    엑셀 파일을 업로드합니다.
    """
    print(f"🍎🍎업로드된 엑셀 파일 이름: {file.filename}")
    return await controller.upload(file)

@router.post("/xbrl/generate")
async def generate_xbrl(request: GenerateRequest):
    """
    XBRL을 생성합니다.
    """
    try:
        result = await controller.generate_xbrl(request.filename, request.data)
        return Response(content=result, media_type="application/xml")
    except Exception as e:
        return {"error": str(e)}

@router.get("/download/{filename}")
async def download_xbrl(filename: str):
    """
    생성된 XBRL 파일을 다운로드합니다.
    """
    file_path = os.path.join("xbrl_output", filename.replace(".xlsx", ".xml"))
    print(f"🍋🍋xml로 변환된 파일 이름: {filename}")
    print(f"🍊🍊xml로 변환된 파일 경로: {file_path}")
    if os.path.exists(file_path):
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            content = await f.read()
            return Response(content=content, media_type="application/xml")
    return {"error": "파일을 찾을 수 없습니다"}

@router.get("/view-xml")
async def view_xbrl_xml():
    """
    생성된 XBRL XML을 HTML 형식으로 조회합니다.
    """
    async with aiofiles.open("xbrl_output/20250421_123650_samsung.xml", "r", encoding="utf-8") as f:
        xml_string = await f.read()
    highlighted = xml_string.replace("<", "&lt;").replace(">", "&gt;")
    return HTMLResponse(content=f"<h2>📄 XBRL XML 결과</h2><pre>{highlighted}</pre>")