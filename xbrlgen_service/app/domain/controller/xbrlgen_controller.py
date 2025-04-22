from fastapi import UploadFile
from app.domain.service.xbrlgen_service import XBRLGenService
import os
from typing import List, Dict, Any

class XBRLGenController:
    def __init__(self):
        self.xbrl_service = XBRLGenService()

    async def upload(self, file: UploadFile):
        return await self.xbrl_service.save_uploaded_excel_file(file)

    async def generate_xbrl(self, filename: str, data: List[Dict[str, Any]]) -> str:
        """
        XBRL을 생성합니다.
        
        Args:
            filename: 업로드된 엑셀 파일명
            data: XBRL 생성에 필요한 데이터
        
        Returns:
            str: 생성된 XBRL XML 문자열
        
        Raises:
            Exception: 파일을 찾을 수 없거나 생성 중 오류가 발생한 경우
        """
        # 업로드된 파일 경로
        excel_path = os.path.join("uploads", filename)
        if not os.path.exists(excel_path):
            raise Exception("업로드된 파일을 찾을 수 없습니다.")
            
        # XBRL 생성 서비스 호출
        return await self.xbrl_service.generate_xbrl(excel_path, filename, data)
