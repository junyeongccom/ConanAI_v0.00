from fastapi import APIRouter, Query
from ..domain.controller.xbrl_parser_controller import XBRLParserController

# 라우터에 명시적으로 태그와 prefix 설정
router = APIRouter(prefix="/xbrl-parser", tags=["XBRL Parser"])
controller = XBRLParserController()

@router.get("/extract")
def extract_files(zip_filename: str = Query(...)):
    result = controller.extract_from_zip(zip_filename)
    return {"status": "success", "extracted_files": result}