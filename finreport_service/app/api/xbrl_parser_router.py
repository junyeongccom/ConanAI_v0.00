from fastapi import APIRouter, Query
from ..domain.controller.xbrl_parser_controller import XBRLParserController

router = APIRouter()
controller = XBRLParserController()

@router.get("/parse")
def parse_xbrl_file(filename: str = Query(..., description="분석할 .xbrl 파일명")):
    result = controller.parse_xbrl_file(filename)
    return {
        "status": "success",
        "file": filename,
        "parsed": result
    }