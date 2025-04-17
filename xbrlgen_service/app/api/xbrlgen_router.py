from fastapi import APIRouter, UploadFile, File
from app.domain.controller.xbrlgen_controller import XBRLGenController

router = APIRouter(prefix="/api/xbrlgen", tags=["XBRL Generation"])
controller = XBRLGenController()

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    return await controller.upload(file)
