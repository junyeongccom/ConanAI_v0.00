from fastapi import APIRouter, UploadFile, File
from app.domain.controller.xbrlgen_controller import XBRLGenController

router = APIRouter(tags=["XBRL Generatior"])
controller = XBRLGenController()

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    return await controller.upload(file)
