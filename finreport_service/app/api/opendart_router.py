from fastapi import APIRouter, Query
from ..domain.controller.opendart_controller import DocumentFetchController

router = APIRouter()
controller = DocumentFetchController()

@router.get("/fetch-xml")
async def fetch_dart_document(
    rcept_no: str = Query(...),
    reprt_code: str = Query("11011")  # 기본값: 사업보고서
):
    path = await controller.fetch_and_store(rcept_no, reprt_code)
    return {"status": "success", "xml_path": path}