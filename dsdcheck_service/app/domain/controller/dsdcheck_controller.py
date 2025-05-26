from typing import Optional
from fastapi import UploadFile

from app.domain.service.dsdcheck_service import DsdCheckService
from app.domain.model.dsdcheck_schema import (
    FinancialDataRequest, 
    FinancialDataResponse,
    FinancialExcelResponse
)


class DsdCheckController:
    """DSD 체크 컨트롤러"""
    
    def __init__(self):
        self.service = DsdCheckService()
    
    async def get_financial_data(self, corp_name: str, year: int) -> Optional[FinancialDataResponse]:
        """
        기업의 연결 및 별도 재무제표 조회
        
        Args:
            corp_name: 기업명
            year: 사업연도
            
        Returns:
            재무제표 응답 또는 None
        """
        request = FinancialDataRequest(corp_name=corp_name, year=year)
        return await self.service.get_financial_data(request)

    async def upload_excel_file(self, file: UploadFile, corp_name: str, year: int) -> Optional[FinancialExcelResponse]:
        """
        업로드된 엑셀 파일에서 재무제표 데이터 추출
        
        Args:
            file: 업로드된 엑셀 파일
            corp_name: 기업명
            year: 기준연도
            
        Returns:
            파싱된 재무제표 응답 또는 None
        """
        return await self.service.parse_uploaded_excel(file, corp_name, year)
