from fastapi import UploadFile
from app.domain.service.xbrlgen_service import XBRLGenService

class XBRLGenController:
    def __init__(self):
        self.service = XBRLGenService()

    async def upload(self, file: UploadFile):
        return await self.service.save_uploaded_excel_file(file)
