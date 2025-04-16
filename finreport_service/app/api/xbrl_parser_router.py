from fastapi import APIRouter, Query
from ..domain.controller.xbrl_parser_controller import XBRLParserController

router = APIRouter(prefix="/xbrl-parser", tags=["XBRL Parser"])
controller = XBRLParserController()

@router.get("/print-balance-tags")
def print_balance_sheet_tags(
    xbrl_filename: str = Query(..., description="XBRL 파일명 (예: entity00165459_2024-12-31)"),
    rcept_no: str = Query(..., description="DART 접수번호 (예: 20250331002860_11011)")
):
    tags = controller.print_balance_sheet_tags(xbrl_filename, rcept_no)
    return {"found_tags": tags}