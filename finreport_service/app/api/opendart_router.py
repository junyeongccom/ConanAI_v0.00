from fastapi import APIRouter, Query
from ..domain.controller.opendart_controller import DocumentFetchController

router = APIRouter(prefix="/opendart")
controller = DocumentFetchController()

@router.get("/fetch-xml")
async def fetch_dart_document(
    rcept_no: str = Query(..., description="DART 접수번호"),
    reprt_code: str = Query("11011", description="보고서 코드 (기본값: 11011, 사업보고서)"),
    auto_extract: bool = Query(True, description="다운로드 후 자동으로 압축 해제할지 여부"),
    delete_zip: bool = Query(True, description="압축 해제 후 원본 ZIP 파일을 삭제할지 여부")
):
    """
    OpenDART에서 XBRL 파일을 다운로드하고 처리합니다.
    
    - auto_extract=True: 압축 해제하여 디렉토리로 저장
    - delete_zip=True: 압축 해제 후 원본 ZIP 삭제
    """
    path = await controller.fetch_and_store(rcept_no, reprt_code, auto_extract, delete_zip)
    
    result = {
        "status": "success",
        "file_type": "directory" if auto_extract else "zip",
        "path": path
    }
    
    return result