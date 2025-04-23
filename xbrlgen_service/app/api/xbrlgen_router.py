from fastapi import APIRouter, UploadFile, File
from app.domain.controller.xbrlgen_controller import XBRLGenController
import os
from fastapi.responses import FileResponse, HTMLResponse
import aiofiles

router = APIRouter(tags=["XBRL Generator"])
controller = XBRLGenController()

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    print(f"🍎🍎업로드된 엑셀 파일 이름: {file.filename}")
    return await controller.upload(file)

@router.get("/download/{filename}")
async def download_xbrl(filename: str):
    file_path = os.path.join("xbrl_output", filename)
    print(f"🍋🍋xml로 변환된 파일 이름: {filename}")
    print(f"🍊🍊xml로 변환된 파일 경로: {file_path}")
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/xml')
    return {"error": "파일을 찾을 수 없습니다"}

@router.get("/view-xml", response_class=HTMLResponse, tags=["Validation Test"])
async def view_xbrl_xml():
    async with aiofiles.open("xbrl_output/20250421_123650_samsung.xml", "r", encoding="utf-8") as f:
        xml_string = await f.read()
    highlighted = xml_string.replace("<", "&lt;").replace(">", "&gt;")
    return f"<h2>📄 XBRL XML 결과</h2><pre>{highlighted}</pre>"