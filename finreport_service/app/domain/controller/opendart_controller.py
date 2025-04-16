from ..service.opendart_service import OpenDartService
import asyncio

class DocumentFetchController:
    def __init__(self):
        self.service = OpenDartService()

    async def fetch_and_store(self, rcept_no: str, reprt_code: str = "11011", auto_extract: bool = True, delete_zip: bool = True) -> str:
        """
        OpenDART에서 XBRL 파일 다운로드 및 저장 처리
        
        Args:
            rcept_no: 접수번호
            reprt_code: 보고서 코드 (기본값: 11011, 사업보고서)
            auto_extract: 다운로드 후 자동으로 압축 해제할지 여부 (기본값: True)
            delete_zip: 압축 해제 후 원본 ZIP 파일을 삭제할지 여부 (기본값: True)
        
        Returns:
            처리된 파일 또는 디렉토리 경로
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            lambda: self.service.fetch_and_store_xbrl(
                rcept_no, 
                reprt_code, 
                auto_extract, 
                delete_zip
            )
        )
