from fastapi import APIRouter, UploadFile, File
from app.domain.controller.xbrlgen_controller import XBRLGenController
import os
from fastapi.responses import FileResponse

router = APIRouter(tags=["XBRL Generatior"])
controller = XBRLGenController()

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    print(f"🍎🍎업로드된 엑셀 파일 이름: {file.filename}")
    return await controller.upload(file)

@router.get("/xbrlgen/download/{filename}", tags=["XBRL Generator"])
async def download_xbrl(filename: str):
    file_path = os.path.join("xbrl_output", filename)
    print(f"🍋🍋xml로 변환된 파일 이름: {filename}")
    print(f"🍊🍊xml로 변환된 파일 경로: {file_path}")
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/xml')
    return {"error": "파일을 찾을 수 없습니다"}
